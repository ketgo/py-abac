"""
    String not contains condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class NotContains(StringCondition):

    def is_satisfied(self, ctx):
        if not is_string(ctx):
            return False
        if self.case_insensitive:
            return self.value.lower() not in ctx.lower()
        return self.value not in ctx


class NotContainsSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotContains(**data)
