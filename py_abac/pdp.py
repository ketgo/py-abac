"""
    Policy decision point implementation
"""

from enum import Enum

from .context import EvaluationContext
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
        Policy decision point
    """

    def __init__(self, storage: StorageBase, algorithm: EvaluationAlgorithm = EvaluationAlgorithm.DENY_OVERRIDES):
        """
            Initialize PDP class object

            :param storage: policy storage
            :param algorithm: evaluation algorithm
        """
        if not isinstance(storage, StorageBase):
            raise TypeError("Invalid type '{}' for storage.".format(type(storage)))
        if not isinstance(algorithm, EvaluationAlgorithm):
            raise TypeError("Invalid type '{}' for evaluation algorithm.".format(type(algorithm)))
        self._storage = storage
        self.algorithm = algorithm

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, alg):
        if alg not in EvaluationAlgorithm:
            raise ValueError("Invalid evaluation algorithm '{}'.".format(alg))
        self._algorithm = alg.value

    def is_allowed(self, request: Request):
        """
            Check if authorization request is allowed

            :param request: request object
            :return: True if authorized else False
        """
        if not isinstance(request, Request):
            raise TypeError("Invalid type '{}' for authorization request.".format(request))

        # Get appropriate evaluation algorithm handler
        evaluate = getattr(self, "_{}".format(self._algorithm))
        # Create evaluation context
        ctx = EvaluationContext(request)

        # Get filtered policies based on targets from storage
        policies = self._storage.get_for_target(ctx.subject_id, ctx.resource_id, ctx.action_id)
        # Filter policies based on fit with authorization request
        policies = [p for p in policies if p.fits(ctx)]

        return evaluate(policies)

    @staticmethod
    def _allow_overrides(policies):
        """
            Allow overrides evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        if not policies:
            return True
        for p in policies:
            if p.is_allowed:
                return True
        return False

    @staticmethod
    def _deny_overrides(policies):
        """
            Deny overrides evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        if not policies:
            return False
        for p in policies:
            if not p.is_allowed:
                return False
        return True

    def _highest_priority(self, policies):
        """
            Highest priority evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        policy_groups = {}
        max_priority = -1
        for p in policies:
            if p.priority > max_priority:
                max_priority = p.priority
            if p.priority in policy_groups:
                policy_groups[p.priority].append(p)
            else:
                policy_groups[p.priority] = []
        return self._deny_overrides(policy_groups[max_priority])
