"""
    All of the values not in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AllNotIn(CollectionCondition):
    """
        Condition for all values of `what` not in `values`
    """

    def _is_satisfied(self, what):
        return not set(what).issubset(self.values)


class AllNotInSchema(CollectionConditionSchema):
    """
        JSON schema for all not in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return AllNotIn(**data)
