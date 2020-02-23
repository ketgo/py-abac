"""
    Value is not in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class IsNotIn(CollectionCondition):
    """
        Condition for `what` is not a member of `values`
    """

    def is_satisfied(self, ctx):
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what):
        return what not in self.values


class IsNotInSchema(CollectionConditionSchema):
    """
        JSON schema for is not in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return IsNotIn(**data)
