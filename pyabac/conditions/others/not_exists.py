"""
    Attribute does not exists condition
"""

from marshmallow import Schema, post_load

from ..base import ConditionBase


class NotExists(ConditionBase):

    def is_satisfied(self, what):
        return what is None


class NotExistsSchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return NotExists()
