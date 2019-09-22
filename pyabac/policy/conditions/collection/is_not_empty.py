"""
    Collection is not empty condition
"""

from marshmallow import Schema, post_load

from .base import ConditionBase, is_collection


class IsNotEmptyCondition(ConditionBase):
    name = "IsNotEmpty"

    def is_satisfied(self, what):
        if not is_collection(what):
            return False
        return len(what) != 0


class IsNotEmptyConditionSchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return IsNotEmptyCondition()
