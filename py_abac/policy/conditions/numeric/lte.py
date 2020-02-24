"""
    Numeric less than equal conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Lte(NumericCondition):
    """
        Condition for number `what` less than equals `value`
    """

    def _is_satisfied(self, what) -> bool:
        return what <= self.value


class LteSchema(NumericConditionSchema):
    """
        JSON schema for less than equals numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Lte(**data)
