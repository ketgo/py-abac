"""
    Collection is not empty conditions
"""

from marshmallow import Schema, post_load

from .base import ConditionBase, is_collection, LOG


class IsNotEmpty(ConditionBase):
    """
        Condition for `what` not being an empty collection
    """

    def is_satisfied(self, ctx):
        if not is_collection(ctx.attribute_value):
            LOG.debug(
                "Invalid type '%s' for attribute value at path '%s' for element '%s'."
                " Condition not satisfied.",
                type(ctx.attribute_value),
                ctx.attribute_path,
                ctx.ace
            )
            return False
        return self._is_satisfied(ctx.attribute_value)

    @staticmethod
    def _is_satisfied(what):
        """
            Is collection conditions satisfied

            :param what: collection to check
            :return: True if satisfied else False
        """
        return len(what) != 0


class IsNotEmptySchema(Schema):
    """
        JSON schema for is not empty collection condition
    """

    @post_load
    def post_load(self, **_):  # pylint: disable=missing-docstring,no-self-use,unused-argument
        return IsNotEmpty()
