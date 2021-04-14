"""
    Any in attribute condition
"""

import logging

from marshmallow import post_load

from .base import AttributeCondition, AttributeConditionSchema
from ..collection.base import is_collection

LOG = logging.getLogger(__name__)


class AnyInAttribute(AttributeCondition):
    """
        Condition for any attribute values in that of another
    """

    def is_satisfied(self, ctx) -> bool:
        # Extract attribute value from request to match
        self.value = ctx.get_attribute_value(self.ace, self.path)
        # Check if attribute value to match is a collection
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

    def _is_satisfied(self, what) -> bool:
        # Check if value is a collection
        if not is_collection(self.value):
            LOG.debug(
                "Invalid type '%s' for attribute value at path '%s' for element '%s'."
                " Condition not satisfied.",
                type(self.value),
                self.path,
                self.ace
            )
            return False
        return bool(set(what).intersection(self.value))


class AnyInAttributeSchema(AttributeConditionSchema):
    """
        JSON schema for any in attribute condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return AnyInAttribute(**data)
