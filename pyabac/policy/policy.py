"""
    Policy class implementation
"""

from marshmallow import Schema, fields, validate, post_load, post_dump

from ..constants import DENY_ACCESS, ALLOW_ACCESS, DEFAULT_POLICY_COLLECTION


class Policy(object):

    def __init__(self, uid, description, subjects, resources, actions, effect, collection=DEFAULT_POLICY_COLLECTION):
        """
            Policy object initialization

            :param uid: policy UID
            :param description: policy description
            :param subjects: list of subject attribute policies
            :param resources: list of resource attribute policies
            :param actions: list of action attribute policies
            :param collection: collection to which this policy belongs
        """
        self.uid = uid or ''
        self.subjects = subjects or []
        self.resources = resources or []
        self.actions = actions or []
        self.effect = effect or DENY_ACCESS
        self.description = description or ''
        self.collection = collection or DEFAULT_POLICY_COLLECTION

    def to_json(self):
        return PolicySchema().dump(self)

    @staticmethod
    def from_json(data):
        return PolicySchema().load(data)

    def fits(self, inquiry):
        """
            Check if this policy fits inquiry

            :param inquiry: inquiry object
            :return: True if fits
        """
        raise NotImplementedError()


class PolicySchema(Schema):
    """
        Policy schema for marshalling
    """

    uid = fields.UUID(required=True, allow_none=False)
    description = fields.String(default="", missing="")
    subjects = fields.List(fields.Dict(required=True, allow_none=False), default=[], missing=[])
    resources = fields.List(fields.Dict(required=True, allow_none=False), default=[], missing=[])
    actions = fields.List(fields.Dict(required=True, allow_none=False), default=[], missing=[])
    context = fields.Dict(default={}, missing={})
    effect = fields.String(required=True, allow_none=False,
                           validate=validate.OneOf(choices=[DENY_ACCESS, ALLOW_ACCESS]))
    collection = fields.String(default=DEFAULT_POLICY_COLLECTION, missing=DEFAULT_POLICY_COLLECTION)

    @post_load
    def post_load(self, data):
        return Policy(**data)

    @post_dump
    def post_dump(self, data):
        return data
