"""
    Numeric less than condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema, is_number


class Lt(NumericCondition):

    def is_satisfied(self, what):
        if not is_number(what):
            return False
        return what < self.value


class LtSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Lt(**data)
