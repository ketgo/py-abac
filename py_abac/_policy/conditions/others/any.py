"""
    Attribute any value conditions
"""
from marshmallow import Schema, post_load

from ..base import ConditionBase


class Any(ConditionBase):
    """
        Condition for attribute having any value
    """

    def is_satisfied(self, ctx) -> bool:
        return True


class AnySchema(Schema):
    """
        JSON schema for any value condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use,unused-argument
        return Any()
