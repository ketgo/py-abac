"""
    Numeric greater than equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema, is_number


class GreaterEqualCondition(NumericCondition):
    name = "GreaterEqual"

    def is_satisfied(self, what):
        if not is_number(what):
            return False
        return what >= self.value


class GreaterEqualConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return GreaterEqualCondition(**data)
