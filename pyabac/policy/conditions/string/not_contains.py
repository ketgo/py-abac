"""
    String not contains condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotContainsCondition(StringCondition):
    name = "StringNotContains"

    def is_satisfied(self, what):
        if self.case_insensitive:
            return self.value.lower() not in what.lower()
        return self.value not in what


class NotContainsConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotContainsCondition(**data)
