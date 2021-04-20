"""
    Is in attribute condition
"""

import logging

from .base import AttributeCondition
from ..collection.base import is_collection

LOG = logging.getLogger(__name__)


class IsInAttribute(AttributeCondition):
    """
        Condition for attribute value in that of another
    """
    # Condition type specifier
    condition: str = "IsInAttribute"

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
        return what in self._value
