"""
    String starts with conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class StartsWith(StringCondition):

    def _is_satisfied(self, what):
        if self.case_insensitive:
            return what.lower().startswith(self.value.lower())
        return what.startswith(self.value)


class StartsWithSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return StartsWith(**data)
