"""
    String starts with condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema, is_string


class StartsWith(StringCondition):

    def is_satisfied(self, what):
        if not is_string(what):
            return False
        if self.case_insensitive:
            return what.lower().startswith(self.value.lower())
        return what.startswith(self.value)


class StartsWithSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return StartsWith(**data)
