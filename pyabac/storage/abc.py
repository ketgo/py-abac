"""
    Wrapper on vakt `Storage` core fields to support policy scoping
"""

from abc import ABCMeta, abstractmethod

from pyabac.common.constants import DEFAULT_POLICY_COLLECTION


class Storage(metaclass=ABCMeta):

    @abstractmethod
    def add(self, policy):
        """
            Store a policy
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self, uid):
        """
            Get specific policy
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all(self, limit, offset, collection=DEFAULT_POLICY_COLLECTION):
        """
            Retrieve all the policies within a window from a policy collection.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_for_inquiry(self, inquiry):
        """
            Get all policies for given inquiry.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, policy):
        """
            Update a policy
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, uid):
        """
            Delete a policy
        """
        raise NotImplementedError()

    @staticmethod
    def _check_limit_and_offset(limit, offset):
        if limit < 0:
            raise ValueError("Limit can't be negative")
        if offset < 0:
            raise ValueError("Offset can't be negative")
