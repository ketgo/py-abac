"""
    Policy decision point implementation
"""

from enum import Enum

from .request import Request
from .storage.base import StorageBase


class EvaluationAlgorithm(Enum):
    """
        Supported evaluation algorithms
    """
    ALLOW_OVERRIDES = "allow_overrides"
    DENY_OVERRIDES = "deny_overrides"
    HIGHEST_PRIORITY = "highest_priority"


class PDP(object):
    """
        Policy decision point class
    """

    def __init__(self, storage: StorageBase):
        """
            Initialize PDP class object

            :param storage: policy storage
        """
        if not isinstance(storage, StorageBase):
            raise TypeError("Invalid type '{}' for storage.".format(type(storage)))
        self._storage = storage

    @property
    def storage(self):
        return self._storage

    def is_allowed(self, request: Request, algorithm: EvaluationAlgorithm):
        """
            Check request authorization

            :param request: request object
            :param algorithm: evaluation algorithm
            :return: True if authorized else False
        """
        if not isinstance(request, Request):
            raise ValueError("Invalid authorization request object '{}'.".format(request))
        if algorithm not in EvaluationAlgorithm:
            raise ValueError("Invalid evaluation algorithm '{}'.".format(algorithm))

        # Get filtered policies based on targets from storage
        policies = self.storage.get_for_target(request.subject_id, request.resource_id, request.action_id)
        # Filter policies based on fit with authorization request
        policies = [p for p in policies if p.fits(request)]

        # Run appropriate evaluation algorithm
        evaluate = getattr(self, "_{}".format(algorithm.value))

        return evaluate(policies)

    @staticmethod
    def _allow_overrides(policies):
        """
            Allow overrides evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        raise NotImplementedError()

    @staticmethod
    def _deny_overrides(policies):
        """
            Deny overrides evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        raise NotImplementedError()

    @staticmethod
    def _highest_priority(policies):
        """
            Highest priority evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        raise NotImplementedError()
