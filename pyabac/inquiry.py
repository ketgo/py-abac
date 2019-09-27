"""
    Inquiry class
"""

from marshmallow import Schema, fields, post_load

from pyabac.constants import DEFAULT_POLICY_COLLECTION


class Inquiry(object):
    """
        Inquiry wrapper class to support policy scope. The default scope is set to `default`.
    """

    def __init__(self, subject=None, resource=None, action=None, context=None, collection=None):
        """
            Inquiry object initialization

            :param subject: subject of inquiry
            :param resource: resource accessed
            :param action: action taken by subject
            :param context: access context
            :param collection: collection of policies to inquire
        """
        self.subject = subject or {}
        self.resource = resource or {}
        self.action = action or {}
        self.context = context or {}
        self.collection = collection or DEFAULT_POLICY_COLLECTION

    def to_json(self):
        return InquirySchema().dump(self)

    @staticmethod
    def from_json(data):
        return InquirySchema().load(data)


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
