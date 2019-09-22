"""
    Policy class implementation
"""
import logging

from jsonpath_ng import parse
from marshmallow import Schema, fields, validate, post_load, post_dump, ValidationError

from .conditions.schema import ConditionSchema
from ..constants import DENY_ACCESS, ALLOW_ACCESS, DEFAULT_POLICY_COLLECTION
from ..exceptions import PolicyCreationError

log = logging.getLogger(__name__)


class Policy(object):

    def __init__(self, uid, description, subjects, resources, actions, context, effect,
                 collection=DEFAULT_POLICY_COLLECTION):
        """
            Policy object initialization

            :param uid: policy UID
            :param description: policy description
            :param subjects: list of subject attribute policies
            :param resources: list of resource attribute policies
            :param actions: list of action attribute policies
            :param context: policy context
            :param effect: effect of policy
            :param collection: collection to which this policy belongs
        """
        self.uid = uid or ''
        self.description = description or ''
        self.subjects = subjects or []
        self.resources = resources or []
        self.actions = actions or []
        self.context = context or {}
        self.effect = effect or DENY_ACCESS
        self.collection = collection or DEFAULT_POLICY_COLLECTION

        # Storing JSON representation of the policy. This performs type checking via marshmallow
        try:
            self._json = PolicySchema().dump(self)
        except ValidationError as err:
            raise PolicyCreationError(*err.args)

    def to_json(self):
        return self._json

    @staticmethod
    def from_json(data):
        try:
            return PolicySchema().load(data)
        except ValidationError as err:
            raise PolicyCreationError(err.args)

    def allow_access(self):
        """
            Does policy imply allow-access?
        """
        return self.effect == ALLOW_ACCESS

    def _fits(self, inquiry):
        """
            Checks if this policy fits inquiry

            :param inquiry: inquiry to check
            :return: True if fits else False
        """
        # Check if any of the subject attribute policies fit the given inquiry
        subject_fits = any(self._attribute_fits(x, inquiry.subject) for x in self.subjects)
        # Check if any of the resource attribute policies fit the given inquiry
        resource_fits = any(self._attribute_fits(x, inquiry.resource) for x in self.resources)
        # Check if any of the action attribute policies fit the given inquiry
        action_fits = any(self._attribute_fits(x, inquiry.action) for x in self.actions)

        return subject_fits and resource_fits and action_fits

    @staticmethod
    def _attribute_fits(field, what):
        """
            Checks if a field's attribute policy fits `what`.

            :param field: definition field of a policy
            :param what: object to check
            :return: True if fits else False
        """
        if not isinstance(field, dict):
            log.error("Incorrect Policy definition. Skipping policy.")
            return False

        checks = []
        for key, value in field.items():
            # Find attribute values from `what` using the path defined in JsonPath format in the policy
            matches = parse(key).find(what)
            for match in matches:
                # Check if the attribute value satisfies the attribute condition policy
                checks.append(value.is_satisfied(match.value))

        # If any attribute does not match the policy then return False
        return all(checks)


def validate_json_path(data):
    """
        Method to check if data is in valid jsonPath format
    """
    try:
        parse(data)
    except Exception as err:
        raise ValidationError(*err.args)


class PolicySchema(Schema):
    """
        Policy schema for marshalling JSON
    """

    uid = fields.UUID(required=True, allow_none=False)
    description = fields.String(default="", missing="")
    subjects = fields.List(
        fields.Mapping(keys=fields.String(required=True, allow_none=False, validate=validate_json_path),
                       values=fields.Nested(ConditionSchema, required=True, allow_none=False, many=False),
                       required=True,
                       allow_none=False),
        default=[],
        missing=[])
    resources = fields.List(
        fields.Mapping(keys=fields.String(required=True, allow_none=False, validate=validate_json_path),
                       values=fields.Nested(ConditionSchema, required=True, allow_none=False, many=False),
                       required=True, allow_none=False),
        default=[],
        missing=[])
    actions = fields.List(
        fields.Mapping(keys=fields.String(required=True, allow_none=False, validate=validate_json_path),
                       values=fields.Nested(ConditionSchema, required=True, allow_none=False, many=False),
                       required=True,
                       allow_none=False),
        default=[],
        missing=[])
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
