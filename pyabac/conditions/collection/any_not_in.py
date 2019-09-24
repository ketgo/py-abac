"""
    Any of the values not in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema, is_collection


class AnyNotInCondition(CollectionCondition):
    name = "AnyNotIn"

    def is_satisfied(self, what):
        # If `what` is not a collection then return False
        if not is_collection(what):
            return False
        return not bool(set(what).intersection(self.value))


class AnyNotInConditionSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AnyNotInCondition(**data)
