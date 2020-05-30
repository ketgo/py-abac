"""
    Policy decision point implementation
"""

from enum import Enum
from typing import List

from .context import EvaluationContext
from .provider.base import AttributeProvider
from .request import AccessRequest
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

        :Example:

        .. code-block:: python

            from py_abac import PDP, EvaluationAlgorithm
            from py_abac.storage import MongoStorage
            from py_abac.providers import AttributeProvider

            # A simple email attribute provider class
            class EmailAttributeProvider(AttributeProvider):
                def get_attribute_value(self, ace, attribute_path, ctx):
                    return "example@gmail.com"

            # Setup storage
            client = MongoClient()
            st = MongoStorage(client)
            # Insert all polices to storage
            for p in policies:
                st.add(p)

            # Create PDP configured to use highest priority algorithm
            # and an additional email attribute provider
            pdp = PDP(st, EvaluationAlgorithm.HIGHEST_PRIORITY, [EmailAttributeProvider()])

        :param storage: policy storage
        :param algorithm: policy evaluation algorithm
        :param providers: list of attribute providers
    """

    def __init__(self,
                 storage: StorageBase,
                 algorithm: EvaluationAlgorithm = EvaluationAlgorithm.DENY_OVERRIDES,
                 providers: List[AttributeProvider] = None):
        if not isinstance(storage, StorageBase):
            raise TypeError("Invalid type '{}' for storage.".format(type(storage)))
        if not isinstance(algorithm, EvaluationAlgorithm):
            raise TypeError("Invalid type '{}' for evaluation algorithm.".format(type(algorithm)))
        self._storage = storage
        self._algorithm = algorithm.value
        self._providers = providers or []
        for provider in self._providers:
            if not isinstance(provider, AttributeProvider):
                raise TypeError("Invalid type '{}' for attribute provider.".format(type(provider)))

    def is_allowed(self, request: AccessRequest):
        """
            Check if authorization request is allowed

            :param request: request object
            :return: True if authorized else False
        """
        if not isinstance(request, AccessRequest):
            raise TypeError("Invalid type '{}' for authorization request.".format(request))

        # Get appropriate evaluation algorithm handler
        evaluate = getattr(self, "_{}".format(self._algorithm))
        # Create evaluation context
        ctx = EvaluationContext(request, self._providers)

        # Get filtered policies based on targets from storage
        policies = self._storage.get_for_target(ctx.subject_id, ctx.resource_id, ctx.action_id)
        # Filter policies based on fit with authorization request
        policies = [policy for policy in policies if policy.fits(ctx)]

        return evaluate(policies)

    @staticmethod
    def _allow_overrides(policies):
        """
            Allow overrides evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        if not policies:
            return False
        for policy in policies:
            if policy.is_allowed:
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
        for policy in policies:
            if not policy.is_allowed:
                return False
        return True

    def _highest_priority(self, policies):
        """
            Highest priority evaluation algorithm

            :param policies: list of policies to evaluate
            :return: True if request is authorized else False
        """
        if not policies:
            return False
        policy_groups = {}
        max_priority = -1
        for policy in policies:
            if policy.priority > max_priority:
                max_priority = policy.priority
            if policy.priority in policy_groups:
                policy_groups[policy.priority].append(policy)
            else:
                policy_groups[policy.priority] = [policy]
        print(policy_groups)
        return self._deny_overrides(policy_groups[max_priority])
