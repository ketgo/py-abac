"""
    String not equals condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotEqualsCondition(StringCondition):
    name = "StringNotEquals"

    def is_satisfied(self, what):
        if self.case_insensitive:
            return what.lower() != self.value.lower()
        return what != self.value


class NotEqualsConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotEqualsCondition(**data)
