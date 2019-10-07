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

        policies = self.storage.get_for_request(request)
        context = EvaluationContext(request)

        return False
