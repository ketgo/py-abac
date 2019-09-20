"""
    Numeric greater than condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class GreaterCondition(NumericCondition):
    name = "Greater"

    def is_satisfied(self, what):
        return what > self.value


class GreaterConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return GreaterCondition(**data)
