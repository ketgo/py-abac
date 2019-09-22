"""
    Numeric equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema, is_number


class EqualCondition(NumericCondition):
    name = "Equal"

    def is_satisfied(self, what):
        if not is_number(what):
            return False
        return what == self.value


class EqualConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return EqualCondition(**data)
