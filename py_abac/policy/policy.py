"""
    Policy class
"""

from marshmallow import Schema, fields, post_load, ValidationError, validate

from .rules import Rules, RulesSchema
from .targets import Targets, TargetsSchema
from ..exceptions import PolicyCreateError
from ..request import Request

# Access decisions
DENY_ACCESS = "deny"
ALLOW_ACCESS = "allow"


class Policy(object):

    def __init__(self, policy_id: str, description: str, rules: Rules, targets: Targets, effect: str,
                 priority: int):
        self.policy_id = policy_id
        self.description = description
        self.rules = rules
        self.targets = targets
        self.effect = effect
        self.priority = priority

    @staticmethod
    def from_json(data: dict):
        try:
            return PolicySchema().load(data)
        except ValidationError as err:
            raise PolicyCreateError(*err.args)

    def to_json(self):
        return PolicySchema().dump(self)

    def fits(self, request: Request):
        """
            Check if the request fits policy

            :param request: authorization request
            :return: Tre if fits else False
        """
        return self.rules.is_satisfied(request) and self.targets.match(request)

    @property
    def is_allowed(self):
        return self.effect == ALLOW_ACCESS


class PolicySchema(Schema):
    policy_id = fields.String(required=True)
    description = fields.String(default="", missing="")
    rules = fields.Nested(RulesSchema, required=True)
    targets = fields.Nested(TargetsSchema, required=True)
    effect = fields.String(required=True, validate=validate.OneOf([DENY_ACCESS, ALLOW_ACCESS]))
    priority = fields.Integer(default=0, missing=0)

    @post_load
    def post_load(self, data, **_):
        return Policy(**data)
