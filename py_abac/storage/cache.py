"""
    Cache for policy storage
"""

import logging
from typing import Union, Generator

from .base import Storage
from .memory import MemoryStorage
from ..policy import Policy

LOG = logging.getLogger(__name__)


class StorageCache(Storage):
    """
        Storage cache for fast policy retrieval.

        :Example:

        .. code-block:: python

            from py_abac.storage.memory

        :param storage: policy storage instance.
        :param cache: policy storage instance acting as cache. Default is set
            to MemoryStorage with `max_size` of 1024.
    """

    def __init__(self, storage: Storage, cache: Storage = MemoryStorage(max_size=1024)):
        self._storage = storage
        self._cache = cache

    def add(self, policy: Policy):
        """
            Store a policy
        """
        self._storage.add(policy)
        self._cache.add(policy)

    def get(self, uid: str) -> Union[Policy, None]:
        """
            Get specific policy
        """
        policy = self._cache.get(uid)
        if not policy:
            LOG.debug("Cache miss occurred. Looking policy from storage.")
            policy = self._storage.get(uid)

        return policy

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        """
            Retrieve all the policies within a window
        """
        # TODO: Sort policies by UID for all storage. This will allow utilization
        #  of any partial results from cache.
        raise NotImplementedError()

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        """
            Get all policies for given target IDs.
        """
        # TODO:
        #  1. Needs a separate cache which indicates if the query is to be run on
        #  cache or backend storage.
        #  2. Need a mechanism to avoid duplicating policy objects in memory since
        #  another cache is introduced. Maybe store only policy UID in the new cache
        raise NotImplementedError()

    def update(self, policy: Policy):
        """
            Update a policy
        """
        self._storage.update(policy)
        self._cache.update(policy)

    def delete(self, uid: str):
        """
            Delete a policy
        """
        self._storage.delete(uid)
        self._cache.delete(uid)
