"""
    Equals object condition
"""

from marshmallow import Schema, fields, post_load

from ..base import ConditionBase


class EqualsObject(ConditionBase):
    """
        Equals object condition
    """

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx):
        return self.value == ctx.attribute_value


class EqualsObjectSchema(Schema):
    value = fields.Dict(required=True)

    @post_load
    def post_load(self, data, **_):
        return EqualsObject(**data)
