"""
    String starts with conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class StartsWith(StringCondition):
    """
        Condition for string `what` starts with `value`
    """

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower().startswith(self.value.lower())
        return what.startswith(self.value)


class StartsWithSchema(StringConditionSchema):
    """
        JSON schema for starts with string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return StartsWith(**data)
