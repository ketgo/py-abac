"""
    String not equals condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class NotEqualsCondition(StringCondition):
    name = "StringNotEquals"

    def is_satisfied(self, what):
        if not is_string(what):
            return False
        if self.case_insensitive:
            return what.lower() != self.value.lower()
        return what != self.value


class NotEqualsConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotEqualsCondition(**data)
