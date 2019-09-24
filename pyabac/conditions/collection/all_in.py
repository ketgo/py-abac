"""
    All of the values in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema, is_collection


class AllInCondition(CollectionCondition):
    name = "AllIn"

    def is_satisfied(self, what):
        # If `what` is not a collection then return False
        if not is_collection(what):
            return False
        return set(what).issubset(self.value)


class AllInConditionSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AllInCondition(**data)
