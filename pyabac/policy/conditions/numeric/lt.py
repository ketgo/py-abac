"""
    Numeric less than condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class LessCondition(NumericCondition):
    name = "Less"

    def is_satisfied(self, what):
        return what < self.value


class LessConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return LessCondition(**data)
