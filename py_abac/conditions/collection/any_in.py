"""
    Any of the values in collection condition
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AnyIn(CollectionCondition):

    def _is_satisfied(self, what):
        return bool(set(what).intersection(self.value))


class AnyInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return AnyIn(**data)
