"""
    Numeric less than equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class LessEqualCondition(NumericCondition):
    name = "LessEqual"

    def is_satisfied(self, what):
        return what <= self.value


class LessEqualConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return LessEqualCondition(**data)
