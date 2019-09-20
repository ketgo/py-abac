"""
    Numeric not equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class NotEqualCondition(NumericCondition):
    name = "NotEqual"

    def is_satisfied(self, what):
        return what != self.value


class NotEqualConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotEqualCondition(**data)
