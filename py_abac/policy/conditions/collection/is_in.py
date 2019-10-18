"""
    Value is in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsIn(CollectionCondition):

    def is_satisfied(self, ctx):
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what):
        return what in self.values


class IsInSchema(CollectionConditionSchema):

    @post_load
    def post_load(self, data, **_):
        return IsIn(**data)
