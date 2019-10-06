"""
    Any of the values not in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema, is_collection


class AnyNotIn(CollectionCondition):

    def is_satisfied(self, ctx):
        # If `what` is not a collection then return False
        if not is_collection(ctx):
            return False
        return not bool(set(ctx).intersection(self.value))


class AnyNotInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AnyNotIn(**data)
