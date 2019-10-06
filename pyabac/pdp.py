"""
    Policy decision point implementation
"""

from enum import Enum

from .context import EvaluationContext
from .storage.base import StorageBase
from .exceptions import InvalidAccessControlElementError


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

    def __init__(self, storage):
        """
            Initialize PDP class object

            :param storage: policy storage
        """
        if not isinstance(storage, StorageBase):
            raise TypeError("Invalid type '{}' for storage.".format(type(storage)))
        self.storage = storage

    def is_allowed(self, request, algorithm):
        """
            Check request authorization

            :param request: request object
            :param algorithm: evaluation algorithm
            :return: True if authorized else False
        """
        if algorithm not in EvaluationAlgorithm:
            raise InvalidAccessControlElementError("Invalid algorithm '{}'.".format(algorithm))

        policies = self.storage.get_for_request(request)
        context = EvaluationContext(request)

        return False
