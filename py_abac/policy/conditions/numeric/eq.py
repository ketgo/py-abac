"""
    Numeric equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Eq(NumericCondition):
    """
        Condition for number `what` equals `value`
    """

    def _is_satisfied(self, what) -> bool:
        return what == self.value


class EqSchema(NumericConditionSchema):
    """
        JSON schema for equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Eq(**data)
