"""
    Numeric greater than conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Gt(NumericCondition):
    """
        Condition for number `what` greater than `value`
    """

    def _is_satisfied(self, what) -> bool:
        return what > self.value


class GtSchema(NumericConditionSchema):
    """
        JSON schema for greater than numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Gt(**data)
