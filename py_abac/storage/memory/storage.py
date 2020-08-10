"""
    In-Memory Storage implementation
"""

from fnmatch import fnmatch
from typing import Generator, Union, Tuple, List

from ..base import Storage
from ...exceptions import PolicyExistsError
from ...policy import Policy


class MemoryStorage(Storage):
    """
        Stores and retrieves policies from memory
    """
    # Default target IDs
    DEFAULT_TARGET_IDS = ("*", "*", "*")

    def __init__(self):
        self._index_map = {}
        self._targets_map = {
            self.DEFAULT_TARGET_IDS: set()
        }

    def add(self, policy: Policy):
        """
            Store a policy
        """
        # Add policy to index map
        if policy.uid in self._index_map:
            raise PolicyExistsError(policy.uid)
        self._index_map[policy.uid] = policy

        for target_ids in self._get_target_ids(
                policy.targets.subject_id,
                policy.targets.resource_id,
                policy.targets.action_id
        ):
            # Add policy UID to targets map
            if target_ids not in self._targets_map:
                self._targets_map[target_ids] = set()
            self._targets_map[target_ids].add(policy.uid)

    def get(self, uid: str) -> Union[Policy, None]:
        """
            Get specific policy
        """
        return self._index_map.get(uid, None)

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        """
            Retrieve all the policies within a window
        """
        self._check_limit_and_offset(limit, offset)
        # Note: python by default sorts dict by key
        keys = list(self._index_map.keys())[offset:offset + limit]
        for key in keys:
            yield self._index_map[key]

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        """
            Get all policies for given target IDs.
        """
        # TODO: Get target IDs from topologically sorted graph for quicker lookup
        for target_ids in self._targets_map:
            matches = [
                fnmatch(subject_id, target_ids[0]),
                fnmatch(resource_id, target_ids[1]),
                fnmatch(action_id, target_ids[2]),
            ]
            if all(matches):
                for uid in self._targets_map[target_ids]:
                    yield self._index_map[uid]

    def update(self, policy: Policy):
        """
            Update a policy
        """
        if policy.uid not in self._index_map:
            raise ValueError("Policy with UID='{}' does not exist.".format(policy.uid))
        self._index_map[policy.uid] = policy

    def delete(self, uid: str):
        """
            Delete a policy
        """
        if uid not in self._index_map:
            raise ValueError("Policy with UID='{}' does not exist.".format(uid))
        target_ids = (
            self._index_map[uid].targets.subject_id,
            self._index_map[uid].targets.resource_id,
            self._index_map[uid].targets.action_id
        )

        # Remove policy from index map
        del self._index_map[uid]

        # Remove policy UID from targets map
        self._targets_map[target_ids].remove(uid)
        if not self._targets_map[target_ids]:
            del self._targets_map[target_ids]

    @staticmethod
    def _get_target_ids(
            subject_ids: Union[List[str], str],
            resource_ids: Union[List[str], str],
            action_ids: Union[List[str], str]
    ) -> Generator[Tuple, None, None]:
        _subject_ids = subject_ids if isinstance(subject_ids, list) else [subject_ids]
        _resource_ids = resource_ids if isinstance(resource_ids, list) else [resource_ids]
        _action_ids = action_ids if isinstance(action_ids, list) else [action_ids]
        for sub_id in _subject_ids:
            for res_id in _resource_ids:
                for act_id in _action_ids:
                    yield sub_id, res_id, act_id
