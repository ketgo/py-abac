"""
    String not contains conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotContains(StringCondition):

    def _is_satisfied(self, what):
        if self.case_insensitive:
            return self.value.lower() not in what.lower()
        return self.value not in what


class NotContainsSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotContains(**data)
