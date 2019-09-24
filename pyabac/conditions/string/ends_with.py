"""
    String ends with condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class EndsWithCondition(StringCondition):
    name = "StringEndsWith"

    def is_satisfied(self, what):
        if not is_string(what):
            return False
        if self.case_insensitive:
            return what.lower().endswith(self.value.lower())
        return what.endswith(self.value)


class EndsWithConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return EndsWithCondition(**data)
