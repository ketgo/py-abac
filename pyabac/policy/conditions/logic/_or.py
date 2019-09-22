"""
    Logical OR condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class OrCondition(LogicCondition):
    name = "Or"

    def is_satisfied(self, what):
        return any(value.is_satisfied(what) for value in self.values)


class OrConditionSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return OrCondition(*data["values"])
