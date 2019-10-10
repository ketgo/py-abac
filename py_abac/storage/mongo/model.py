"""
    MongoDB policy storage model
"""

import json
import re

from ...policy import Policy
from ...policy.targets import Targets


def _split_id(wc_id: str) -> list:
    """
        This method splits a wildcard-ed ID `wc_id` in such a way that if `wc_id`
        matches an arbitrary string, then all its members also match that string.
        This is achieved by splitting the ID by the wildcard "*". Furthermore, each
        member of the split is prefixed and suffixed with the wildcard, depending
        on the location of the wildcard itself.

            Examples:
                "ab*c" -> ["ab*", "*c"]
                "*a*b" -> ["*a*", "*b"]
                "ab**" -> ["ab*"]

        See unit tests for more examples.
    """
    # Remove consecutive wildcard duplicates, e.g. ab** -> ab*
    _string = wc_id
    for rep in re.findall(r"\*\**", wc_id):
        _string = _string.replace(rep, "*")

    # Split if wildcard is in string and length of string is greater than 1 character
    if "*" in _string and len(_string) > 1:
        # Adjust string start index if wildcard present as first character
        start = 1 if _string[0] == "*" else 0
        # Adjust string end index if wildcard present as last character
        end = len(_string) - 1 if _string[-1] == "*" else len(_string)
        # Split adjusted string by wildcard
        splits = _string[start:end].split("*")
        # Compensate the starting member of the split due to adjusted string
        splits[0] = _string[:start] + splits[0]
        for x in range(len(splits) - 1):
            # Add wildcard as suffix
            splits[x] = splits[x] + "*"
            # Add wildcard as prefix of the next member
            splits[x + 1] = "*" + splits[x + 1]
        # Compensate the last member of the split due to adjusted string
        splits[-1] = splits[-1] + _string[end:]

        return splits

    return [_string]


def _get_all_ids(target_id: str) -> list:
    """
        This method computes all possible wildcard-ed IDs for a given target ID.

            Examples:


        See unit tests for more examples.
    """
    rvalue = {target_id: True}
    length = len(target_id)
    # Compute all N-grams
    for N in range(length):
        # Compute N-grams
        size = length - N
        span = N + 1
        rvalue["*" + target_id[:span] + "*"] = True
        rvalue[target_id[:span] + "*"] = True
        for i in range(1, size - 1):
            rvalue["*" + target_id[i:i + span] + "*"] = True
        rvalue["*" + target_id[size - 1:size - 1 + span]] = True
        rvalue["*" + target_id[size - 1:size - 1 + span] + "*"] = True

    return list(rvalue.keys())


class PolicyModel(object):
    """
        Model to store policy as document on MongoDB
    """

    def __init__(self, _id: str, policy_str: str, tags: dict):
        """
            Initialize mongodb document

            :param _id: document ID
            :param policy_str: policy JSON string
            :param tags: tags for target based filtering
        """
        self._id = _id
        self.policy_str = policy_str
        self.tags = tags

    @classmethod
    def from_policy(cls, policy: Policy):
        policy_str = json.dumps(policy.to_json())
        tags = cls._targets_to_tags(policy.targets)
        return cls(policy.uid, policy_str, tags)

    def to_policy(self):
        policy_json = json.loads(self.policy_str)
        return Policy.from_json(policy_json)

    @classmethod
    def from_doc(cls, data):
        return cls(**data)

    def to_doc(self):
        return self.__dict__

    @staticmethod
    def get_filter_query(subject_id: str, resource_id: str, action_id: str):
        """
            Get query using target ids to retrieve policies
        """
        return {"subject": {"$elemMatch": {"$in": _get_all_ids(subject_id)}},
                "resource": {"$elemMatch": {"$in": _get_all_ids(resource_id)}},
                "action": {"$elemMatch": {"$in": _get_all_ids(action_id)}}}

    @staticmethod
    def _targets_to_tags(targets: Targets):
        wc_subject_ids = targets.subject_id if isinstance(targets.subject_id, list) else [targets.subject_id]
        wc_resource_ids = targets.resource_id if isinstance(targets.resource_id, list) else [targets.resource_id]
        wc_action_ids = targets.action_id if isinstance(targets.action_id, list) else [targets.action_id]
        return {"subject": [{"id": _split_id(x)} for x in wc_subject_ids],
                "resource": [{"id": _split_id(x)} for x in wc_resource_ids],
                "action": [{"id": _split_id(x)} for x in wc_action_ids]}
