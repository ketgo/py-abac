"""
    String starts with condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class StartsWithCondition(StringCondition):
    name = "StringStartsWith"

    def is_satisfied(self, what):
        if self.case_insensitive:
            return what.lower().startswith(self.value.lower())
        return what.startswith(self.value)


class StartsWithConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return StartsWithCondition(**data)
