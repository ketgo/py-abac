"""
    Value is not in collection condition
"""

from marshmallow import Schema, fields, post_load

from .base import ConditionBase


class IsNotIn(ConditionBase):

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx):
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what):
        return what not in self.value


class IsNotInSchema(Schema):
    value = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)

    @post_load
    def post_load(self, data, **_):
        return IsNotIn(**data)