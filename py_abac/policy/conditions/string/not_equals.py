"""
    String not equals conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotEquals(StringCondition):

    def _is_satisfied(self, what):
        if self.case_insensitive:
            return what.lower() != self.value.lower()
        return what != self.value


class NotEqualsSchema(StringConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return NotEquals(**data)
