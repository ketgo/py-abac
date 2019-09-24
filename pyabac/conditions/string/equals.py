"""
    String equals condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class EqualsCondition(StringCondition):
    name = "StringEquals"

    def is_satisfied(self, what):
        if not is_string(what):
            return False
        if self.case_insensitive:
            return what.lower() == self.value.lower()
        return what == self.value


class EqualsConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return EqualsCondition(**data)
