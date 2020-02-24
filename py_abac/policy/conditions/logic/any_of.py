"""
    Logical OR conditions
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class AnyOf(LogicCondition):
    """
        Condition for any of sub-rules are satisfied
    """

    def is_satisfied(self, ctx) -> bool:
        return any(value.is_satisfied(ctx) for value in self.values)


class AnyOfSchema(LogicConditionSchema):
    """
        JSON schema for any of logical condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return AnyOf(**data)
