"""
    String ends with conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class EndsWith(StringCondition):
    """
        Condition for string `what` ends with `value`
    """

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower().endswith(self.value.lower())
        return what.endswith(self.value)


class EndsWithSchema(StringConditionSchema):
    """
        JSON schema for ends with string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return EndsWith(**data)
