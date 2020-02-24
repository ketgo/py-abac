"""
    Numeric not equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Neq(NumericCondition):
    """
        Condition for number `what` not equals `value`
    """

    def _is_satisfied(self, what) -> bool:
        return what != self.value


class NeqSchema(NumericConditionSchema):
    """
        JSON schema for not equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Neq(**data)
