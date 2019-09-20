"""
    Logical all condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class AllCondition(LogicCondition):
    name = "All"

    def is_satisfied(self, what):
        return all(value.is_satisfied(what) for value in self.values)


class AllConditionSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AllCondition(*data["values"])
