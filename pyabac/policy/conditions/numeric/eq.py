"""
    Numeric equal condition
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class EqualCondition(NumericCondition):
    name = "Equal"

    def is_satisfied(self, what):
        return what == self.value


class EqualConditionSchema(NumericConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return EqualCondition(**data)
