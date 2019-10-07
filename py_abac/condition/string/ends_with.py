"""
    String ends with condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class EndsWith(StringCondition):

    def _is_satisfied(self, what):
        if self.case_insensitive:
            return what.lower().endswith(self.value.lower())
        return what.endswith(self.value)


class EndsWithSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return EndsWith(**data)
