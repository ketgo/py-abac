"""
    All of the values in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AllIn(CollectionCondition):

    def _is_satisfied(self, what):
        return set(what).issubset(self.values)


class AllInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AllIn(**data)
