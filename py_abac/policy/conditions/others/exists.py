"""
    Attribute exists conditions
"""
from marshmallow import Schema, post_load

from ..base import ConditionBase


class Exists(ConditionBase):

    def is_satisfied(self, ctx):
        return ctx.attribute_value is not None


class ExistsSchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return Exists()
