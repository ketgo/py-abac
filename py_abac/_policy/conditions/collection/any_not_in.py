"""
    Any of the values not in collection conditions
"""

from marshmallow import post_load

from .base import CollectionCondition, CollectionConditionSchema


class AnyNotIn(CollectionCondition):
    """
        Condition for any values of `what` not in `values`
    """

    def _is_satisfied(self, what) -> bool:
        return not bool(set(what).intersection(self.values))


class AnyNotInSchema(CollectionConditionSchema):
    """
        JSON schema for any not in collection condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return AnyNotIn(**data)
