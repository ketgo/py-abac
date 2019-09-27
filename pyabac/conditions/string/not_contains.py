"""
    String not contains condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class NotContains(StringCondition):

    def is_satisfied(self, what):
        if not is_string(what):
            return False
        if self.case_insensitive:
            return self.value.lower() not in what.lower()
        return self.value not in what


class NotContainsSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotContains(**data)
