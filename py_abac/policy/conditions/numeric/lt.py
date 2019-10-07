"""
    Numeric less than conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Lt(NumericCondition):

    def _is_satisfied(self, what):
        return what < self.value


class LtSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Lt(**data)
