"""
    Equals object conditions
"""

from marshmallow import Schema, fields, post_load

from ..base import ConditionBase


class EqualsObject(ConditionBase):
    """
        Equals object conditions
    """

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx) -> bool:
        return self.value == ctx.attribute_value


class EqualsObjectSchema(Schema):
    """
        JSON schema for equals object condition
    """
    value = fields.Dict(required=True)

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return EqualsObject(**data)
