"""
    Any not in attribute condition
"""

import logging

from .base import AttributeCondition
from ..collection.base import is_collection

LOG = logging.getLogger(__name__)


class AnyNotInAttribute(AttributeCondition):
    """
        Condition for any attribute values not in that of another
    """
    # Condition type specifier
    condition: str = "AnyNotInAttribute"

    def is_satisfied(self, ctx) -> bool:
        # Extract attribute value from request to match
        self._value = ctx.get_attribute_value(self.ace, self.path)
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
        if not is_collection(self._value):
            LOG.debug(
                "Invalid type '%s' for attribute value at path '%s' for element '%s'."
                " Condition not satisfied.",
                type(self._value),
                self.path,
                self.ace
            )
            return False
        return not bool(set(what).intersection(self._value))
