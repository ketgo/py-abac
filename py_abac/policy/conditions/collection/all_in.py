"""
    All of the values in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AllIn(CollectionCondition):
    """
        Condition for all values of `what` in `values`
    """

    def _is_satisfied(self, what):
        return set(what).issubset(self.values)


class AllInSchema(CollectionConditionSchema):
    """
        JSON schema for all in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return AllIn(**data)
