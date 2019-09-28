"""
    Value is not in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsNotIn(CollectionCondition):

    def is_satisfied(self, what):
        return what not in self.value


class IsNotInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return IsNotIn(**data)
