"""
    Any of the values not in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AnyNotIn(CollectionCondition):

    def _is_satisfied(self, what):
        return not bool(set(what).intersection(self.values))


class AnyNotInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AnyNotIn(**data)
