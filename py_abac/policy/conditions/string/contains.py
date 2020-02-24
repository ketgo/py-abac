"""
    String contains conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class Contains(StringCondition):
    """
        Condition for string `what` contains `value`
    """

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return self.value.lower() in what.lower()
        return self.value in what


class ContainsSchema(StringConditionSchema):
    """
        JSON schema for contains string conditions
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Contains(**data)
