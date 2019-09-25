"""
    Logical OR condition
"""

from marshmallow import post_load

from .base import LogicCondition, LogicConditionSchema


class Or(LogicCondition):

    def is_satisfied(self, what):
        return any(value.is_satisfied(what) for value in self.values)


class OrSchema(LogicConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return Or(*data["values"])
