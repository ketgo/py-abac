"""
    Numeric not equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema, is_number


class Neq(NumericCondition):

    def is_satisfied(self, what):
        if not is_number(what):
            return False
        return what != self.value


class NeqSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Neq(**data)
