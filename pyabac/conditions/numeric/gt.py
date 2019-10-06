"""
    Numeric greater than condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Gt(NumericCondition):

    def _is_satisfied(self, value):
        return value > self.value


class GtSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Gt(**data)
