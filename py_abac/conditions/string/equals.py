"""
    String equals condition
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class Equals(StringCondition):

    def _is_satisfied(self, what):
        if self.case_insensitive:
            return what.lower() == self.value.lower()
        return what == self.value


class EqualsSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Equals(**data)
