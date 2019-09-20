"""
    String contains condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class ContainsCondition(StringCondition):
    name = "StringContains"

    def is_satisfied(self, what):
        if self.case_insensitive:
            return self.value.lower() in what.lower()
        return self.value in what


class ContainsConditionSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return ContainsCondition(**data)
