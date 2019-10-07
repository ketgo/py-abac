"""
    PDP policy evaluation context
"""

from ..request import Request


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
        # Access control element being evaluated
        self._ace = None
        # Path of attribute being evaluated
        self._attribute_path = None

    @property
    def request(self):
        return self._request

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
        return self.request.get_value(self.ace, self.attribute_path)
