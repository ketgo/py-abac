"""
    Authorization request class
"""

from marshmallow import Schema, fields, ValidationError, post_load
from objectpath import Tree

from .exceptions import RequestCreateError, InvalidAccessControlElementError, InvalidAttributePathError


class Request(object):
    """
        Authorization request sent by PEP
    """

    def __init__(self, subject: dict, resource: dict, action: dict, context: dict):

        self._subject_id = subject.get("id", "")
        self._subject_tree = Tree(subject.get("attributes", {}))

        self._resource_id = resource.get("id", "")
        self._resource_tree = Tree(resource.get("attributes", {}))

        self._action_id = action.get("id", "")
        self._action_tree = Tree(action.get("attributes", {}))

        self._context_tree = Tree(context)

        # Cache of attribute location and value pairs per access element used for quick attribute value retrieval
        self._attribute_values_cache = {"subject": {}, "resource": {}, "action": {}, "context": {}}

    @staticmethod
    def from_json(data: dict):
        try:
            return _RequestSchema().load(data)
        except ValidationError as err:
            raise RequestCreateError(*err.args)

    @property
    def subject_id(self):
        return self._subject_id

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def action_id(self):
        return self._action_id

    def get_value(self, ace: str, path: str):
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
    attributes = fields.Dict(default={}, missing={})


class _RequestSchema(Schema):
    """
            JSON schema for authorization request
        """
    subject = fields.Nested(_AccessElementSchema, required=True)
    resource = fields.Nested(_AccessElementSchema, required=True)
    action = fields.Nested(_AccessElementSchema, required=True)
    context = fields.Dict(default={}, missing={})

    @post_load
    def post_load(self, data, **_):
        return Request(**data)
