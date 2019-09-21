"""
    Wrapper on vakt `Storage` core fields to support policy scoping
"""

from abc import ABCMeta, abstractmethod

from ..constants import DEFAULT_POLICY_COLLECTION


class Storage(metaclass=ABCMeta):

    @abstractmethod
    def add(self, policy):
        """
            Store a policy
        """
        pass

    @abstractmethod
    def get(self, uid):
        """
            Get specific policy
        """
        pass

    @abstractmethod
    def get_all(self, limit, offset, collection=DEFAULT_POLICY_COLLECTION):
        """
            Retrieve all the policies within a window from a policy collection.
        """
        pass

    @abstractmethod
    def get_for_inquiry(self, inquiry):
        """
            Get all policies for given inquiry.
        """
        pass

    @abstractmethod
    def update(self, policy):
        """
            Update a policy
        """
        pass

    @abstractmethod
    def delete(self, uid):
        """
            Delete a policy
        """
        pass

    @staticmethod
    def _check_limit_and_offset(limit, offset):
        if limit < 0:
            raise ValueError("Limit can't be negative")
        if offset < 0:
            raise ValueError("Offset can't be negative")
