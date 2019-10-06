"""
    Numeric not equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Neq(NumericCondition):

    def _is_satisfied(self, value):
        return value != self.value


class NeqSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Neq(**data)
