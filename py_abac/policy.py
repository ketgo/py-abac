"""
    Policy class implementation
"""

import logging
import uuid

from marshmallow import Schema, fields, validate, post_load, ValidationError
from objectpath import Tree

from py_abac.common.constants import DENY_ACCESS, ALLOW_ACCESS, DEFAULT_POLICY_COLLECTION
from py_abac.common.exceptions import PolicyCreationError
from py_abac.conditions.base import ConditionBase
from py_abac.conditions.schema import ConditionSchema

log = logging.getLogger(__name__)


def validate_object_path(path):
    try:
        Tree({}).execute(path)
    except Exception:
        raise ValidationError("Invalid object path '{}'.".format(path))


class Policy(object):

    def __init__(self, uid=None, description=None, subjects=None, resources=None, actions=None, context=None,
                 effect=None, collection=DEFAULT_POLICY_COLLECTION, _validate=True):
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
            :param _validate: flag to validate input
        """
        self.uid = uid or str(uuid.uuid4())
        self.description = description or ''
        self.subjects = subjects or []
        self.resources = resources or []
        self.actions = actions or []
        self.context = context or {}
        self.effect = effect or DENY_ACCESS
        self.collection = collection or DEFAULT_POLICY_COLLECTION

        # Validate policy definition
        if _validate:
            self._validate()

    def _validate(self):
        self._validate_element('subjects', self.subjects, True)
        self._validate_element('resources', self.resources, True)
        self._validate_element('actions', self.actions, True)
        self._validate_element('context', self.context, False)
        if self.effect not in [ALLOW_ACCESS, DENY_ACCESS]:
            raise PolicyCreationError("Invalid access type '{}'.".format(self.effect))

    @staticmethod
    def _validate_element(name, value, many=False):
        """
            Method to check if policy field is valid

            :param name: name of element
            :param value: value for policy element
            :param many: flag to indicate list of values
            :raises: ValidationError
        """
        _value = value if many else [value]
        if not isinstance(_value, list):
            raise PolicyCreationError("Invalid policy definition.")
        for v in _value:
            if not isinstance(v, dict):
                raise PolicyCreationError("Invalid type '{}' for policy field '{}'.".format(type(v), name))
            for k in v:
                try:
                    validate_object_path(k)
                except ValidationError:
                    raise PolicyCreationError("Invalid JSON path '{}' for attribute.".format(k))
                if not isinstance(v[k], ConditionBase):
                    raise PolicyCreationError("Invalid type '{}' for field attribute '{}'.".format(type(v[k]), k))

    def to_json(self):
        return PolicySchema().dump(self)

    @staticmethod
    def from_json(data):
        try:
            return PolicySchema().load(data)
        except ValidationError as err:
            raise PolicyCreationError(*err.args)

    def allow_access(self):
        """
            Does policy imply allow-access?
        """
        return self.effect == ALLOW_ACCESS


class PolicySchema(Schema):
    """
        Policy schema for marshalling JSON
    """

    uid = fields.String(required=True, allow_none=False)
    description = fields.String(default="", missing="")
    subjects = fields.List(
        fields.Dict(keys=fields.String(validate=validate_object_path), values=fields.Nested(ConditionSchema)),
        default=[],
        missing=[])
    resources = fields.List(
        fields.Dict(keys=fields.String(validate=validate_object_path), values=fields.Nested(ConditionSchema)),
        default=[],
        missing=[])
    actions = fields.List(
        fields.Dict(keys=fields.String(validate=validate_object_path), values=fields.Nested(ConditionSchema)),
        default=[],
        missing=[])
    context = fields.Dict(keys=fields.String(validate=validate_object_path), values=fields.Nested(ConditionSchema),
                          default={}, missing={})
    effect = fields.String(required=True, allow_none=False,
                           validate=validate.OneOf(choices=[DENY_ACCESS, ALLOW_ACCESS]))
    collection = fields.String(default=DEFAULT_POLICY_COLLECTION, missing=DEFAULT_POLICY_COLLECTION)

    @post_load
    def post_load(self, data, **_):
        return Policy(**data, _validate=False)
