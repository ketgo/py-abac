"""
    Numeric less than equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Lte(NumericCondition):

    def _is_satisfied(self, what):
        return what <= self.value


class LteSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Lte(**data)
