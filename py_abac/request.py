"""
    Authorization request class
"""

from typing import Dict

from marshmallow import Schema, fields, validate, ValidationError, post_load

from .exceptions import RequestCreateError


class AccessRequest(object):
    """
        Authorization request sent by PEP

        :Example:

        .. code-block:: python

            # Create a access request JSON from flask request object
            request_json = {
                "subject": {
                    "id": "",
                    "attributes": {"name": request.values.get("username")}
                },
                "resource": {
                    "id": "",
                    "attributes": {"name": request.path}
                },
                "action": {
                    "id": "",
                    "attributes": {"method": request.method}
                },
                "context": {}
            }
            # Parse JSON and create access request object
            request = AccessRequest.from_json(request_json)
    """

    def __init__(self, subject: dict, resource: dict, action: dict, context: dict):
        # Request subject identifier
        self._subject_id = subject.get("id", "")
        # Request subject attributes
        self._subject = subject.get("attributes", {})

        # Requested resource identifier
        self._resource_id = resource.get("id", "")
        # Requested resource attributes
        self._resource = resource.get("attributes", {})

        # Request action identifier
        self._action_id = action.get("id", "")
        # Request action attributes
        self._action = action.get("attributes", {})

        # Request context attributes
        self._context = context

    @property
    def subject_id(self) -> str:
        """
            Request subject identifier
        """
        return self._subject_id

    @property
    def subject(self) -> Dict:
        """
            Request subject attributes
        """
        return self._subject

    @property
    def resource_id(self) -> str:
        """
            Requested resource identifier
        """
        return self._resource_id

    @property
    def resource(self) -> Dict:
        """
            Requested resource attributes
        """
        return self._resource

    @property
    def action_id(self) -> str:
        """
            Request action identifier
        """
        return self._action_id

    @property
    def action(self) -> Dict:
        """
            Request action attributes
        """
        return self._action

    @property
    def context(self):
        """
            Request context attributes
        """
        return self._context

    @staticmethod
    def from_json(data: dict) -> "AccessRequest":
        """
            Create access request object from JSON
        """
        try:
            return _RequestSchema().load(data)
        except ValidationError as err:
            raise RequestCreateError(*err.args)


# backward compatible with v0.2.0
Request = AccessRequest


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
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return AccessRequest(**data)
