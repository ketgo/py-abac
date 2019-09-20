"""
    Numeric greater than equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class GreaterEqualCondition(NumericCondition):
    name = "GreaterEqual"

    def is_satisfied(self, what):
        return what >= self.value


class GreaterEqualConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return GreaterEqualCondition(**data)
