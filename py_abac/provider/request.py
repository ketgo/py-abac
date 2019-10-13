"""
    Request attribute provider implementation
"""

from objectpath import Tree

from .base import AttributeProvider
from ..exceptions import InvalidAccessControlElementError, InvalidAttributePathError
from ..request import Request


class RequestAttributeProvider(AttributeProvider):
    """
        Request attribute provider
    """

    def __init__(self, request: Request):
        """
            Initialize attribute provider

            :param request: authorization request object
        """

        self._subject_tree = Tree(request._subject)
        self._resource_tree = Tree(request._resource)
        self._action_tree = Tree(request._action)
        self._context_tree = Tree(request._context)

        # Cache of attribute location and value pairs per access element used for quick attribute value retrieval
        self._attribute_values_cache = {"subject": {}, "resource": {}, "action": {}, "context": {}}

    def get_attribute_value(self, ace, path, ctx):
        # Validates given access control element and gets ObjectPath tree
        try:
            attribute_tree = getattr(self, "_{}_tree".format(ace))
        except AttributeError:
            raise InvalidAccessControlElementError(ace)

        # Check if attribute value stored in cache
        if path in self._attribute_values_cache[ace]:
            rvalue = self._attribute_values_cache[ace][path]
        else:
            # Attribute value not found in cache so get it from ObjectPath tree
            try:
                rvalue = attribute_tree.execute(path)
            # Broad exception needed for ObjectPath package
            except Exception:
                raise InvalidAttributePathError(path)
            # Store the obtained value in cache
            self._attribute_values_cache[ace][path] = rvalue
        return rvalue
