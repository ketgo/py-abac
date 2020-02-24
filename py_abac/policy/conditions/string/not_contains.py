"""
    String not contains conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotContains(StringCondition):
    """
        Condition for string `what` not contains `value`
    """

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return self.value.lower() not in what.lower()
        return self.value not in what


class NotContainsSchema(StringConditionSchema):
    """
        JSON schema for not contains string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return NotContains(**data)
