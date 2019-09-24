"""
    Value is in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsInCondition(CollectionCondition):
    name = "IsIn"

    def is_satisfied(self, what):
        return what in self.value


class IsInConditionSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return IsInCondition(**data)
