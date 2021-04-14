"""
    Logical AND conditions
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class AllOf(LogicCondition):
    """
        Condition for all of the sub-rules are satisfied
    """

    def is_satisfied(self, ctx) -> bool:
        return all(value.is_satisfied(ctx) for value in self.values)


class AllOfSchema(LogicConditionSchema):
    """
        JSON schema for all of logical condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return AllOf(**data)
