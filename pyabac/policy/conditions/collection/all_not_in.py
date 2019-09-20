"""
    All of the values not in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema, is_collection


class AllNotInCondition(CollectionCondition):
    name = "AllNotIn"

    def is_satisfied(self, what):
        if not is_collection(what):
            raise TypeError("Value should be of list type")
        return not set(what).issubset(self.value)


class AllNotInConditionSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AllNotInCondition(**data)
