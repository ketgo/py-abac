"""
    Attribute any value condition
"""
from marshmallow import Schema, post_load

from ..base import ConditionBase


class Any(ConditionBase):

    def is_satisfied(self, ctx):
        return True


class AnySchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return Any()
