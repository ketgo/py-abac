"""
    String starts with condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class StartsWith(StringCondition):

    def is_satisfied(self, ctx):
        if not is_string(ctx):
            return False
        if self.case_insensitive:
            return ctx.lower().startswith(self.value.lower())
        return ctx.startswith(self.value)


class StartsWithSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return StartsWith(**data)
