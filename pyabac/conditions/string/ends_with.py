"""
    String ends with condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class EndsWith(StringCondition):

    def is_satisfied(self, ctx):
        if not is_string(ctx):
            return False
        if self.case_insensitive:
            return ctx.lower().endswith(self.value.lower())
        return ctx.endswith(self.value)


class EndsWithSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return EndsWith(**data)
