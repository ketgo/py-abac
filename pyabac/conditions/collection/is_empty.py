"""
    Collection is empty condition
"""

from marshmallow import Schema, post_load

from .base import ConditionBase, is_collection


class IsEmpty(ConditionBase):

    def is_satisfied(self, ctx):
        if not is_collection(ctx):
            return False
        return len(ctx) == 0


class IsEmptySchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return IsEmpty()
