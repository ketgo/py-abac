"""
    Attribute does not exists conditions
"""

from marshmallow import Schema, post_load

from ..base import ConditionBase


class NotExists(ConditionBase):

    def is_satisfied(self, ctx):
        return ctx.attribute_value is None


class NotExistsSchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return NotExists()
