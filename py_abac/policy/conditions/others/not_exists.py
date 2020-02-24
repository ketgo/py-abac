"""
    Attribute does not exists conditions
"""

from marshmallow import Schema, post_load

from ..base import ConditionBase


class NotExists(ConditionBase):
    """
        Condition for attribute value not exists
    """

    def is_satisfied(self, ctx) -> bool:
        return ctx.attribute_value is None


class NotExistsSchema(Schema):
    """
        JSON schema for attribute value not exists condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use,unused-argument
        return NotExists()
