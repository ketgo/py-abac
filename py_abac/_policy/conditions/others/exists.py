"""
    Attribute exists conditions
"""
from marshmallow import Schema, post_load

from ..base import ConditionBase


class Exists(ConditionBase):
    """
        Condition for attribute value exists
    """

    def is_satisfied(self, ctx) -> bool:
        return ctx.attribute_value is not None


class ExistsSchema(Schema):
    """
        JSON schema for attribute value exists conditions
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use,unused-argument
        return Exists()
