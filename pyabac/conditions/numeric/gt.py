"""
    Numeric greater than condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema, is_number


class Gt(NumericCondition):

    def is_satisfied(self, what):
        if not is_number(what):
            return False
        return what > self.value


class GtSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Gt(**data)
