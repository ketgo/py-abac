"""
    Logical any condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class AnyCondition(LogicCondition):
    name = "Any"

    def is_satisfied(self, what):
        return any(value.is_satisfied(what) for value in self.values)


class AnyConditionSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AnyCondition(*data["values"])
