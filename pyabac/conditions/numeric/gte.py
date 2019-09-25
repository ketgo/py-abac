"""
    Numeric greater than equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema, is_number


class Gte(NumericCondition):

    def is_satisfied(self, what):
        if not is_number(what):
            return False
        return what >= self.value


class GteSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Gte(**data)
