"""
    Attribute exists condition
"""
from marshmallow import Schema, post_load

from .base import ConditionBase


class ExistsCondition(ConditionBase):
    name = "Exists"

    def is_satisfied(self, what):
        return what is not None


class ExistsConditionSchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return ExistsCondition()


class NotExistsCondition(ConditionBase):
    name = "NotExists"

    def is_satisfied(self, what):
        return what is None


class NotExistsConditionSchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return NotExistsCondition()
