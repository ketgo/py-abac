"""
    Collection is not empty conditions
"""

from marshmallow import Schema, post_load

from .base import ConditionBase, is_collection, LOG


class IsNotEmpty(ConditionBase):

    def is_satisfied(self, ctx):
        if not is_collection(ctx.attribute_value):
            LOG.debug("Invalid type '{}' for attribute value at path '{}' for element '{}'. "
                      "Condition not satisfied.".format(ctx.attribute_value, ctx.attribute_path, ctx.ace))
            return False
        return self._is_satisfied(ctx.attribute_value)

    @staticmethod
    def _is_satisfied(what):
        return len(what) != 0


class IsNotEmptySchema(Schema):

    @post_load
    def post_load(self, data, **_):
        return IsNotEmpty()
