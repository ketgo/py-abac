"""
    PDP policy evaluation context
"""

from .request import Request


class EvaluationContext(object):
    """
        Evaluation context class
    """

    def __init__(self, request: Request):
        """
            Initialize evaluation context object

            :param request: request object
        """
        if not isinstance(request, Request):
            raise TypeError("Invalid type '{}' for authorization request.".format(type(request)))
        self._request = request
        # TODO: Other attribute value providers as part of PIP
        self._providers = []  # pragma: no cover
        # Access control element being evaluated
        self._ace = None
        # Path of attribute being evaluated
        self._attribute_path = None

    @property
    def subject_id(self):
        return self._request._subject_id

    @property
    def resource_id(self):
        return self._request._resource_id

    @property
    def action_id(self):
        return self._request._action_id

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
        # TODO: Add attribute value providers as part of PIP
        return self._request.get_value(ace, attribute_path)
