"""
    Collection is empty condition
"""

from marshmallow import Schema, post_load

from .base import ConditionBase, is_collection


class IsEmpty(ConditionBase):

    def is_satisfied(self, what):
        if not is_collection(what):
            return False
        return len(what) == 0


class IsEmptySchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return IsEmpty()
