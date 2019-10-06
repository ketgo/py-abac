"""
    Any of the values in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema, is_collection


class AnyIn(CollectionCondition):

    def is_satisfied(self, ctx):
        # If `what` is not a collection then return False
        if not is_collection(ctx):
            return False
        return bool(set(ctx).intersection(self.value))


class AnyInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AnyIn(**data)
