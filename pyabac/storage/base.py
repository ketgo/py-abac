"""
    Policy Storage abstract class
"""

from abc import ABCMeta, abstractmethod


class StorageBase(metaclass=ABCMeta):

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
    def get_all(self, limit, offset):
        """
            Retrieve all the policies within a window
        """
        raise NotImplementedError()

    @abstractmethod
    def get_for_request(self, request):
        """
            Get all policies for given request.
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
