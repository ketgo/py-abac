"""
    Numeric greater than equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Gte(NumericCondition):

    def _is_satisfied(self, what):
        return what >= self.value


class GteSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Gte(**data)
