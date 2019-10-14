"""
    Numeric greater than conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Gt(NumericCondition):

    def _is_satisfied(self, what):
        return what > self.value


class GtSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Gt(**data)
