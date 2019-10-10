"""
    Policy Storage abstract class
"""

from types import GeneratorType
from abc import ABCMeta, abstractmethod

from ..policy import Policy


class StorageBase(metaclass=ABCMeta):

    @abstractmethod
    def add(self, policy: Policy):
        """
            Store a policy
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self, uid: str) -> Policy:
        """
            Get specific policy
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all(self, limit: int, offset: int) -> GeneratorType:
        """
            Retrieve all the policies within a window
        """
        raise NotImplementedError()

    @abstractmethod
    def get_for_target(self, subject_id: str, resource_id: str, action_id: str) -> GeneratorType:
        """
            Get all policies for given target IDs.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, policy: Policy):
        """
            Update a policy
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, uid: str):
        """
            Delete a policy
        """
        raise NotImplementedError()

    @staticmethod
    def _check_limit_and_offset(limit: int, offset: int):
        if limit < 0:
            raise ValueError("Limit can't be negative")
        if offset < 0:
            raise ValueError("Offset can't be negative")
