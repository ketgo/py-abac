"""
    Attribute any value condition
"""
from marshmallow import Schema, post_load

from ..base import ConditionBase


class AnyValueCondition(ConditionBase):
    name = "AnyValue"

    def is_satisfied(self, what):
        return True


class AnyValueConditionSchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return AnyValueCondition()
