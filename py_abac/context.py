"""
    PDP policy evaluation context
"""

import logging
from typing import List, Any

from .provider.base import AttributeProvider
from .provider.request import RequestAttributeProvider
from .request import Request

LOG = logging.getLogger(__name__)


class EvaluationContext(object):
    """
        Evaluation context class
    """

    def __init__(self, request: Request, providers: List[AttributeProvider] = None):
        """
            Initialize evaluation context object

            :param request: request object
        """
        self._subject_id = request.subject_id
        self._resource_id = request.resource_id
        self._action_id = request.action_id
        self._request_provider = RequestAttributeProvider(request)
        self._other_providers = providers or []

        # Access control element being evaluated
        self._ace = None
        # Path of attribute being evaluated
        self._attribute_path = None
        # Call stack of attribute providers as called by context. The stack
        # is used to prevent infinite recursive loops.
        self._provider_call_stack = [None]

    @property
    def subject_id(self) -> str:
        """
            Subject identifier being evaluated
        """
        return self._subject_id

    @property
    def resource_id(self) -> str:
        """
            Resource identifier being evaluated
        """
        return self._resource_id

    @property
    def action_id(self):
        """
            Action identifier being evaluated
        """
        return self._action_id

    @property
    def ace(self) -> str:
        """
            Access control element being evaluated
        """
        return self._ace

    @ace.setter
    def ace(self, value: str):
        """
            Set access control element to evaluate
        """
        self._ace = value

    @property
    def attribute_path(self) -> str:
        """
            Attribute path being evaluated in ObjectPath notation
        """
        return self._attribute_path

    @attribute_path.setter
    def attribute_path(self, path: str):
        """
            Set attribute path to evaluate
        """
        self._attribute_path = path

    @property
    def attribute_value(self) -> Any:
        """
            Attribute value to evaluate
        """
        return self.get_attribute_value(self.ace, self.attribute_path)

    def get_attribute_value(self, ace: str, attribute_path: str):
        """
            Get attribute value for given access control element and attribute path

            :param ace: access control element
            :param attribute_path: attribute path in ObjectPath format
            :return: attribute value
        """
        rvalue = self._request_provider.get_attribute_value(ace, attribute_path, self)
        # If attribute value not found then check other attribute providers
        if rvalue is None:
            # Providers are checked in order
            for provider in self._other_providers:
                # To prevent infinite recursion skip provider if already in call stack.
                if provider not in self._provider_call_stack:
                    # Append provider to call-stack
                    self._provider_call_stack.append(provider)
                    # Call attribute provider
                    rvalue = provider.get_attribute_value(ace, attribute_path, self)
                    # Pop provider from call-stack
                    self._provider_call_stack.pop()
                    if rvalue is not None:
                        # Return attribute value for the very first provider which has the value.
                        # Other providers are not checked.
                        return rvalue
        return rvalue
