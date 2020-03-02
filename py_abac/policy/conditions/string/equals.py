"""
    String equals conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class Equals(StringCondition):
    """
        Condition for string `what` equals `value`
    """

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower() == self.value.lower()
        return what == self.value


class EqualsSchema(StringConditionSchema):
    """
        JSON schema for equals string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Equals(**data)
