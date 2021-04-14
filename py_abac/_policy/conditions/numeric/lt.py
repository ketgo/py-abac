"""
    Numeric less than conditions
"""

from marshmallow import post_load

from .base import NumericCondition, NumericConditionSchema


class Lt(NumericCondition):
    """
        Condition for number `what` less than `value`
    """

    def _is_satisfied(self, what) -> bool:
        return what < self.value


class LtSchema(NumericConditionSchema):
    """
        JSON schema for less than numeric condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Lt(**data)
