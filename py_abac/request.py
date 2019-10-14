"""
    Authorization request class
"""

from marshmallow import Schema, fields, validate, ValidationError, post_load

from .exceptions import RequestCreateError


class Request(object):
    """
        Authorization request sent by PEP
    """

    def __init__(self, subject: dict, resource: dict, action: dict, context: dict):

        self._subject_id = subject.get("id", "")
        self._subject = subject.get("attributes", {})

        self._resource_id = resource.get("id", "")
        self._resource = resource.get("attributes", {})

        self._action_id = action.get("id", "")
        self._action = action.get("attributes", {})

        self._context = context

        # Cache of attribute location and value pairs per access element used for quick attribute value retrieval
        self._attribute_values_cache = {"subject": {}, "resource": {}, "action": {}, "context": {}}

    @staticmethod
    def from_json(data: dict):
        try:
            return _RequestSchema().load(data)
        except ValidationError as err:
            raise RequestCreateError(*err.args)


class _AccessElementSchema(Schema):
    """
        JSON schema for access element
    """
    id = fields.String(required=True, validate=validate.Length(max=400))
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
