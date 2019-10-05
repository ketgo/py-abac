"""
    Inquiry class
"""

from marshmallow import Schema, fields, post_load, ValidationError

from pyabac.common.constants import DEFAULT_POLICY_COLLECTION
from pyabac.common.exceptions import InquiryCreationError


class Inquiry(object):
    """
        Inquiry class implementation.
    """

    def __init__(self, subject=None, resource=None, action=None, context=None, collection=None, _validate=True):
        """
            Inquiry object initialization

            :param subject: subject of inquiry
            :param resource: resource accessed
            :param action: action taken by subject
            :param context: access context
            :param collection: collection of policies to inquire
            :param _validate: flag to validate input
        """
        self.subject = subject or {}
        self.resource = resource or {}
        self.action = action or {}
        self.context = context or {}
        self.collection = collection or DEFAULT_POLICY_COLLECTION

        if _validate:
            self._validate()

    def _validate(self):
        if not isinstance(self.subject, dict):
            raise InquiryCreationError("Invalid type '{}' for subject.".format(type(self.subject)))
        if not isinstance(self.resource, dict):
            raise InquiryCreationError("Invalid type '{}' for resource.".format(type(self.resource)))
        if not isinstance(self.action, dict):
            raise InquiryCreationError("Invalid type '{}' for action.".format(type(self.action)))
        if not isinstance(self.context, dict):
            raise InquiryCreationError("Invalid type '{}' for context.".format(type(self.context)))
        if not isinstance(self.collection, str):
            raise InquiryCreationError("Invalid collection '{}'.".format(self.collection))

    def to_json(self):
        return InquirySchema().dump(self)

    @staticmethod
    def from_json(data):
        try:
            return InquirySchema().load(data)
        except ValidationError as err:
            raise InquiryCreationError(*err.args)


class InquirySchema(Schema):
    """
        Inquiry schema for marshalling
    """

    subject = fields.Dict(default={}, missing={})
    resource = fields.Dict(default={}, missing={})
    action = fields.Dict(default={}, missing={})
    context = fields.Dict(default={}, missing={})
    collection = fields.String(default=DEFAULT_POLICY_COLLECTION, missing=DEFAULT_POLICY_COLLECTION)

    @post_load
    def post_load(self, data, **_):
        return Inquiry(**data)
