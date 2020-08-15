"""
    In-Memory Storage implementation
"""

import logging
from itertools import islice
from typing import Generator, Union

from lru import LRU

from ..base import Storage
from ...exceptions import PolicyExistsError
from ...policy import Policy

LOG = logging.getLogger(__name__)


class MemoryStorage(Storage):
    """
        Stores and retrieves policies from memory

        :param max_size: maximum number of polices to store by the
            storage. Default is set to `None` which results in no
            upper bound.
    """

    def __init__(self, max_size: int = None):
        self._index_map = LRU(max_size) if max_size else {}

    def add(self, policy: Policy):
        """
            Store a policy
        """
        # Add policy to index map
        if policy.uid in self._index_map:
            raise PolicyExistsError(policy.uid)
        self._index_map[policy.uid] = policy
        LOG.info('Added Policy: %s', policy)

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
        policies = islice(self._index_map.values(), offset, offset + limit)
        for policy in policies:
            yield policy

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        """
            Get all policies for given target IDs.

            .. note:

                Currently all policies are returned for evaluation.
        """
        # TODO: Create glob match based topologically sorted graph index for filtering
        for policy in self._index_map.values():
            yield policy

    def update(self, policy: Policy):
        """
            Update a policy
        """
        if policy.uid not in self._index_map:
            raise ValueError("Policy with UID='{}' does not exist.".format(policy.uid))
        self._index_map[policy.uid] = policy
        LOG.info('Updated Policy with UID=%s. New value is: %s', policy.uid, policy)

    def delete(self, uid: str):
        """
            Delete a policy
        """
        if uid not in self._index_map:
            raise ValueError("Policy with UID='{}' does not exist.".format(uid))
        # Remove policy from index map
        del self._index_map[uid]
        LOG.info('Deleted Policy with UID=%s.', uid)
