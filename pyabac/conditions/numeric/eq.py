"""
    Numeric equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Eq(NumericCondition):

    def _is_satisfied(self, value):
        return value == self.value


class EqSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Eq(**data)
