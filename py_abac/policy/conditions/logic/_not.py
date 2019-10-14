"""
    Logical NOT conditions
"""

from marshmallow import Schema, fields, post_load

from .base import ConditionBase


class Not(ConditionBase):

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx):
        return not self.value.is_satisfied(ctx)


class NotSchema(Schema):
    value = fields.Nested("ConditionSchema", required=True, allow_none=False, many=False)

    @post_load
    def post_load(self, data, **_):
        return Not(**data)
