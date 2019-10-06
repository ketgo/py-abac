"""
    All of the values not in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema, is_collection


class AllNotIn(CollectionCondition):

    def is_satisfied(self, ctx):
        # If `what` is not a collection then return False
        if not is_collection(ctx):
            return False
        return not set(ctx).issubset(self.value)


class AllNotInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AllNotIn(**data)
