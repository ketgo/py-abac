"""
    Logical OR condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class AnyOf(LogicCondition):

    def is_satisfied(self, ctx):
        return any(value.is_satisfied(ctx) for value in self.values)


class AnyOfSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AnyOf(*data["values"])
