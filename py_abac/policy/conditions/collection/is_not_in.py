"""
    Value is not in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsNotIn(CollectionCondition):

    def is_satisfied(self, ctx):
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what):
        return what not in self.values


class IsNotInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return IsNotIn(**data)
