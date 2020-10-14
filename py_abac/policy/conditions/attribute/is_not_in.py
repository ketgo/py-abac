"""
    Is not in attribute condition
"""

import logging

from marshmallow import post_load

from .base import AttributeCondition, AttributeConditionSchema
from ..collection.base import is_collection

LOG = logging.getLogger(__name__)


class IsNotInAttribute(AttributeCondition):
    """
        Condition for attribute value not in that of another
    """

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
        return what not in self.value


class IsNotInAttributeSchema(AttributeConditionSchema):
    """
        JSON schema for is not in attribute condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return IsNotInAttribute(**data)
