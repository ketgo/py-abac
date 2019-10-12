"""
    PDP policy evaluation context
"""

from typing import List

from .provider.base import AttributeProvider
from .provider.request import RequestAttributeProvider
from .request import Request


class EvaluationContext(object):
    """
        Evaluation context class
    """

    def __init__(self, request: Request, providers: List[AttributeProvider] = None):
        """
            Initialize evaluation context object

            :param request: request object
        """
        self._subject_id = request._subject_id
        self._resource_id = request._resource_id
        self._action_id = request._action_id
        self._request_provider = RequestAttributeProvider(request)
        self._other_providers = providers or []

        # Access control element being evaluated
        self._ace = None
        # Path of attribute being evaluated
        self._attribute_path = None

    @property
    def subject_id(self):
        return self._subject_id

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def action_id(self):
        return self._action_id

    @property
    def ace(self):
        return self._ace

    @ace.setter
    def ace(self, value: str):
        self._ace = value

    @property
    def attribute_path(self):
        return self._attribute_path

    @attribute_path.setter
    def attribute_path(self, path: str):
        self._attribute_path = path

    @property
    def attribute_value(self):
        return self.get_attribute_value(self.ace, self.attribute_path)

    def get_attribute_value(self, ace: str, attribute_path: str):
        """
            Get attribute value for given access control element and attribute path

            :param ace: access control element
            :param attribute_path: attribute path in ObjectPath format
            :return: attribute value
        """
        rvalue = self._request_provider.get_attribute_value(ace, attribute_path)
        # If attribute value not found then check other attribute providers
        if not rvalue:
            # Providers are checked in order
            for provider in self._other_providers:
                rvalue = provider.get_attribute_value(ace, attribute_path)
                if rvalue:
                    # Return attribute value for the very first provider which has the value.
                    # Other providers are not checked.
                    return rvalue
        return rvalue
