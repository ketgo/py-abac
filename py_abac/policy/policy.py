"""
    Policy class
"""

from marshmallow import Schema, fields, post_load, ValidationError, validate

from py_abac.context import EvaluationContext
from .rules import Rules, RulesSchema
from .targets import Targets, TargetsSchema
from ..exceptions import PolicyCreateError

# Access decisions
DENY_ACCESS = "deny"
ALLOW_ACCESS = "allow"


class Policy(object):

    def __init__(self, uid: str, description: str, rules: Rules, targets: Targets, effect: str,
                 priority: int):
        self.uid = uid
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

    def fits(self, ctx: EvaluationContext):
        """
            Check if the request fits policy

            :param ctx: evaluation context
            :return: Tre if fits else False
        """
        return self.rules.is_satisfied(ctx) and self.targets.match(ctx)

    @property
    def is_allowed(self):
        return self.effect == ALLOW_ACCESS


class PolicySchema(Schema):
    uid = fields.String(required=True)
    description = fields.String(default="", missing="")
    rules = fields.Nested(RulesSchema, required=True)
    targets = fields.Nested(TargetsSchema, required=True)
    effect = fields.String(required=True, validate=validate.OneOf([DENY_ACCESS, ALLOW_ACCESS]))
    priority = fields.Integer(default=0, missing=0, validate=validate.Range(min=0))

    @post_load
    def post_load(self, data, **_):
        return Policy(**data)
