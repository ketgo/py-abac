"""
    Cache for policy storage
"""

from typing import Union, Generator

from .base import StorageBase
from ..policy import Policy


class StorageCache(StorageBase):
    """
        Storage cache for fast policy retrieval.

        :Example:

        .. code-block:: python

        :param storage: policy storage instance.
        :param max_size: maximum size of the cache. The size
            represents number of policies stored.
    """

    def __init__(self, storage: StorageBase, max_size: int = 1024):
        self._storage = storage
        self._max_size = max_size

    def add(self, policy: Policy):
        """
            Store a policy
        """
        raise NotImplementedError()

    def get(self, uid: str) -> Union[Policy, None]:
        """
            Get specific policy
        """
        raise NotImplementedError()

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        """
            Retrieve all the policies within a window
        """
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
        raise NotImplementedError()

    def update(self, policy: Policy):
        """
            Update a policy
        """
        raise NotImplementedError()

    def delete(self, uid: str):
        """
            Delete a policy
        """
        raise NotImplementedError()
