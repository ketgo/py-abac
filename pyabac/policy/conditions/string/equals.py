"""
    String equals condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class EqualsCondition(StringCondition):
    name = "StringEquals"

    def is_satisfied(self, what):
        if self.case_insensitive:
            return what.lower() == self.value.lower()
        return what == self.value


class EqualsConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return EqualsCondition(**data)
