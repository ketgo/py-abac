"""
    Value is in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsIn(CollectionCondition):

    def is_satisfied(self, ctx):
        return ctx in self.value


class IsInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return IsIn(**data)
