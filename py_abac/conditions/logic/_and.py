"""
    Logical AND condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class And(LogicCondition):

    def is_satisfied(self, what):
        return all(value.is_satisfied(what) for value in self.values)


class AndSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return And(*data["values"])
