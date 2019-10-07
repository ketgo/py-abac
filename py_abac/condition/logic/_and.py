"""
    Logical AND condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class AllOf(LogicCondition):

    def is_satisfied(self, ctx):
        return all(value.is_satisfied(ctx) for value in self.values)


class AllOfSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AllOf(**data)
