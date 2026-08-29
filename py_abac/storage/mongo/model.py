"""
    MongoDB policy storage model
"""

import json

from ..utils import get_sub_wildcard_queries, get_all_wildcard_queries, has_untranslatable_wildcard
from ...policy import Policy
from ...policy.targets import Targets


class PolicyModel:
    """
        Model to store policy as document on MongoDB.

        :param _id: document ID
        :param policy_str: policy JSON string
        :param tags: tags for target based filtering
    """

    def __init__(self, _id: str, policy_str: str, tags: dict = None):
        self._id = _id
        self.policy_str = policy_str
        self.tags = tags

    @classmethod
    def from_policy(cls, policy: Policy):
        """
            Create model instance from policy object
        """
        policy_str = json.dumps(policy.to_json())
        tags = cls._targets_to_tags(policy.targets)
        return cls(policy.uid, policy_str, tags)

    def to_policy(self):
        """
            Get policy object
        """
        policy_json = json.loads(self.policy_str)
        return Policy.from_json(policy_json)

    @classmethod
    def from_doc(cls, data):
        """
            Create policy model from MongoDB document
        """
        return cls(**data)

    def to_doc(self):
        """
            Get MongoDB document
        """
        return self.__dict__

    @staticmethod
    def get_aggregate_pipeline(subject_id: str, resource_id: str, action_id: str):
        """
            Get query using target ids to retrieve policies
        """
        # Compute all wildcard queries from target IDs
        subject_wildcard_queries = get_all_wildcard_queries(subject_id)
        resource_wildcard_queries = get_all_wildcard_queries(resource_id)
        action_wildcard_queries = get_all_wildcard_queries(action_id)
        # Stage 1 filter query which utilizes indexes: Checks if any member
        # in tags is member of wildcard queries set
        stage_1 = {
            "$match": {
                "tags.subject.id": {"$in": subject_wildcard_queries},
                "tags.resource.id": {"$in": resource_wildcard_queries},
                "tags.action.id": {"$in": action_wildcard_queries}
            }
        }
        # Stage 2 filter query for subset match: Checks if tags is subset of
        # wildcard query set
        stage_2 = {
            "$match": {
                "tags.subject.id": {"$not": {"$elemMatch": {"$nin": subject_wildcard_queries}}},
                "tags.resource.id": {"$not": {"$elemMatch": {"$nin": resource_wildcard_queries}}},
                "tags.action.id": {"$not": {"$elemMatch": {"$nin": action_wildcard_queries}}}
            }
        }
        return [stage_1, stage_2]

    @staticmethod
    def _targets_to_tags(targets: Targets):
        subject_queries = targets.subject_id \
            if isinstance(targets.subject_id, list) else [targets.subject_id]
        resource_queries = targets.resource_id \
            if isinstance(targets.resource_id, list) else [targets.resource_id]
        action_queries = targets.action_id \
            if isinstance(targets.action_id, list) else [targets.action_id]
        # Add all wildcard sub-queries for target queries. '?' and '[seq]' have no
        # equivalent in the tag-based wildcard grammar (which only understands '*')
        # and would otherwise be tagged as literal strings, silently dropping the
        # policy from `get_for_target()` results (GHSA-rq77-w5m2-2g6m). Widen such
        # targets to match everything; `Targets.match()` re-checks with fnmatch.
        def _tag_queries(queries):
            return [["*"] if has_untranslatable_wildcard(x) else get_sub_wildcard_queries(x) for x in queries]

        return {
            "subject": [{"id": q} for q in _tag_queries(subject_queries)],
            "resource": [{"id": q} for q in _tag_queries(resource_queries)],
            "action": [{"id": q} for q in _tag_queries(action_queries)]
        }
