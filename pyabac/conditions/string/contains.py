"""
    String contains condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class Contains(StringCondition):

    def is_satisfied(self, ctx):
        if not is_string(ctx):
            return False
        if self.case_insensitive:
            return self.value.lower() in ctx.lower()
        return self.value in ctx


class ContainsSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Contains(**data)
