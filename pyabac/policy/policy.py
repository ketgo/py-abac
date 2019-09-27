"""
    Policy class implementation
"""

import logging
import uuid

from jsonpath_ng import parse
from marshmallow import Schema, fields, validate, post_load, ValidationError

from pyabac.constants import DENY_ACCESS, ALLOW_ACCESS, DEFAULT_POLICY_COLLECTION
from pyabac.exceptions import PolicyCreationError
from pyabac.conditions.base import ConditionBase
from pyabac.conditions.schema import ConditionSchema

log = logging.getLogger(__name__)


def _validate_json_path(path):
    """
        Method to check if path is in valid jsonPath format

        :param path: json path to validate
        :raises: ValidationError
    """
    try:
        parse(path)
    except Exception as err:
        raise ValidationError(*err.args)


def _validate_field(name, value, many=False):
    """
        Method to check if policy field is valid

        :param name: name of field
        :param value: value for policy field
        :param many: flag to indicate list of values
        :raises: ValidationError
    """
    _value = value if many else [value]
    if not isinstance(_value, list):
        raise ValidationError("Invalid policy definition.")
    for v in _value:
        if not isinstance(v, dict):
            raise ValidationError("Invalid type '{}' for policy field '{}'.".format(type(v), name))
        for k in v:
            _validate_json_path(k)
            if not isinstance(v[k], ConditionBase):
                raise ValidationError("Invalid type '{}' for field attribute '{}'.".format(type(v[k]), k))


class Policy(object):

    def __init__(self, uid=None, description=None, subjects=None, resources=None, actions=None, context=None,
                 effect=None, collection=DEFAULT_POLICY_COLLECTION):
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
        self.uid = uid or str(uuid.uuid4())
        self.description = description or ''
        self.subjects = subjects or []
        self.resources = resources or []
        self.actions = actions or []
        self.context = context or {}
        self.effect = effect or DENY_ACCESS
        self.collection = collection or DEFAULT_POLICY_COLLECTION

        # Validate policy definition
        self._validate()

    def to_json(self):
        return PolicySchema().dump(self)

    @staticmethod
    def from_json(data):
        try:
            return PolicySchema().load(data)
        except Exception as err:
            raise PolicyCreationError(*err.args)

    def allow_access(self):
        """
            Does policy imply allow-access?
        """
        return self.effect == ALLOW_ACCESS

    def fits(self, inquiry):
        """
            Checks if this policy fits inquiry

            :param inquiry: inquiry to check
            :return: True if fits else False
        """
        # Check if any of the subject attributes fit the policy
        if not self._field_fits(self.subjects, inquiry.subject):
            return False
        # Check if any of the resource attributes fit the policy
        if not self._field_fits(self.resources, inquiry.resource):
            return False
        # Check if any of the action attributes fit the policy
        if not self._field_fits(self.actions, inquiry.action):
            return False
        # Check if any of the context attributes fit policy
        if not self._query_fits(self.context, inquiry.context):
            return False
        # If the policy fits then return True
        return True

    def _field_fits(self, field, what):
        """
            Checks if a policy field fits `what`

            :param field: policy field
            :param what: object to check
            :return: True if fits else False
        """
        for query in field:
            # If any of the query fits inquiry then return True
            if self._query_fits(query, what):
                return True
        # If no query fits inquiry then return False
        return False

    @staticmethod
    def _query_fits(query, what):
        """
            Checks if a policy field's query fits `what`.

            :param query: policy field query
            :param what: object to check
            :return: True if fits else False
        """
        for attr_path, condition in query.items():
            # Find attribute values from `what` using the path defined in JsonPath format in the policy.
            # If no path found then set the value to `None`.
            matches = parse(attr_path).find(what)
            values = [match.value for match in matches] if matches else [None]
            # Check all extracted values
            for value in values:
                # Check if the extracted value satisfies the condition for field's attribute. If any
                # attribute does not match the policy then return False.
                if not condition.is_satisfied(value):
                    return False
        # If all attributes match the policy then return True
        return True

    def _validate(self):
        """
            Validate Policy definition
            :raises: PolicyCreationError
        """
        try:
            _validate_field('subjects', self.subjects, True)
            _validate_field('resources', self.resources, True)
            _validate_field('actions', self.actions, True)
            _validate_field('context', self.context, False)
            if self.effect not in [ALLOW_ACCESS, DENY_ACCESS]:
                raise ValidationError("Invalid access type '{}'.".format(self.effect))
        except ValidationError as err:
            raise PolicyCreationError(*err.args)


class PolicySchema(Schema):
    """
        Policy schema for marshalling JSON
    """

    uid = fields.String(required=True, allow_none=False)
    description = fields.String(default="", missing="")
    subjects = fields.List(
        fields.Dict(keys=fields.String(validate=_validate_json_path), values=fields.Nested(ConditionSchema)),
        default=[],
        missing=[])
    resources = fields.List(
        fields.Dict(keys=fields.String(validate=_validate_json_path), values=fields.Nested(ConditionSchema)),
        default=[],
        missing=[])
    actions = fields.List(
        fields.Dict(keys=fields.String(validate=_validate_json_path), values=fields.Nested(ConditionSchema)),
        default=[],
        missing=[])
    context = fields.Dict(keys=fields.String(validate=_validate_json_path), values=fields.Raw(),
                          default={}, missing={})
    effect = fields.String(required=True, allow_none=False,
                           validate=validate.OneOf(choices=[DENY_ACCESS, ALLOW_ACCESS]))
    collection = fields.String(default=DEFAULT_POLICY_COLLECTION, missing=DEFAULT_POLICY_COLLECTION)

    @post_load
    def post_load(self, data, **_):
        return Policy(**data)
