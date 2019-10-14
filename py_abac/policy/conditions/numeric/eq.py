"""
    Numeric equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Eq(NumericCondition):

    def _is_satisfied(self, what):
        return what == self.value


class EqSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Eq(**data)
