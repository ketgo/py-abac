"""
    All of the values not in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AllNotIn(CollectionCondition):

    def _is_satisfied(self, what):
        return not set(what).issubset(self.values)


class AllNotInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AllNotIn(**data)
