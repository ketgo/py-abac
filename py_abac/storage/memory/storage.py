"""
    In-Memory Storage implementation
"""

from typing import Generator

from ..base import StorageBase
from ...policy import Policy


class MemoryStorage(StorageBase):
    """
        Stores and retrieves policies from memory
    """

    def add(self, policy: Policy):
        """
            Store a policy
        """
        pass

    def get(self, uid: str) -> Policy:
        """
            Get specific policy
        """
        pass

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        """
            Retrieve all the policies within a window
        """
        pass

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        """
            Get all policies for given target IDs.
        """
        pass

    def update(self, policy: Policy):
        """
            Update a policy
        """
        pass

    def delete(self, uid: str):
        """
            Delete a policy
        """
        pass
