"""
    Value is in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsIn(CollectionCondition):
    """
        Condition for `what` is a member of `values`
    """

    def is_satisfied(self, ctx):
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what) -> bool:
        return what in self.values


class IsInSchema(CollectionConditionSchema):
    """
        JSON schema for is in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return IsIn(**data)
