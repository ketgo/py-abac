"""
    String not equals conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotEquals(StringCondition):
    """
        Condition for string `what` not equals `value`
    """

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower() != self.value.lower()
        return what != self.value


class NotEqualsSchema(StringConditionSchema):
    """
        JSON schema for not equals string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return NotEquals(**data)
