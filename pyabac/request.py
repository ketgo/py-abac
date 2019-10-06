"""
    Authorization request class
"""

from marshmallow import Schema, fields, ValidationError
from objectpath import Tree

from .exceptions import RequestCreateError, InvalidAccessControlElementError, InvalidAttributePathError


class Request(object):
    """
        Authorization request sent by PEP
    """

    def __init__(self, data):
        try:
            _data = _RequestSchema().load(data)
        except ValidationError as err:
            raise RequestCreateError(*err.args)

        self._subject_id = _data.get("subject", {}).get("id", "")
        self._subject_tree = Tree(_data.get("subject", {}).get("attributes", {}))

        self._resource_id = _data.get("resource", {}).get("id", "")
        self._resource_tree = Tree(_data.get("resource", {}).get("attributes", {}))

        self._action_id = _data.get("action", {}).get("id", "")
        self._action_tree = Tree(_data.get("action", {}).get("attributes", {}))

        self._context_tree = Tree(_data.get("context", {}))

        # Cache of attribute location and value pairs per access element used for quick attribute value retrieval
        self._attribute_values_cache = {"subject": {}, "resource": {}, "action": {}, "context": {}}

    @property
    def subject_id(self):
        return self._subject_id

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def action_id(self):
        return self._action_id

    def get_value(self, ace, path):
        """
            Get attribute value for given access control element and attribute path

            :param ace: access control element
            :param path: attribute path in ObjectPath format
            :return: attribute value
        """
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


class _AccessElementSchema(Schema):
    """
        JSON schema for access element
    """
    id = fields.String(required=True)
    attributes = fields.Dict(required=True)


class _RequestSchema(Schema):
    """
            JSON schema for authorization request
        """
    subject = fields.Nested(_AccessElementSchema, required=True)
    resource = fields.Nested(_AccessElementSchema, required=True)
    action = fields.Nested(_AccessElementSchema, required=True)
    context = fields.Dict(required=True)
