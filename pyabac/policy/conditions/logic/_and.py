"""
    Logical AND condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class AndCondition(LogicCondition):
    name = "And"

    def is_satisfied(self, what):
        return all(value.is_satisfied(what) for value in self.values)


class AndConditionSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AndCondition(*data["values"])
