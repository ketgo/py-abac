"""
    Numeric conditions base class
"""

import logging

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


def is_number(value) -> bool:
    """
        Check if value is a number
    """
    return isinstance(value, (float, int))


class NumericCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for numeric conditions
    """

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx) -> bool:
        if not is_number(ctx.attribute_value):
            LOG.debug(
                "Invalid type '%s' for attribute value at path '%s' for element '%s'."
                " Condition not satisfied.",
                type(ctx.attribute_value),
                ctx.attribute_path,
                ctx.ace
            )
            return False
        return self._is_satisfied(ctx.attribute_value)

    @abstractmethod
    def _is_satisfied(self, what) -> bool:
        """
            Is numeric conditions satisfied

            :param what: numeric value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class NumericConditionSchema(Schema):
    """
        Base JSON schema for numeric conditions
    """
    value = fields.Number(required=True, allow_none=False)
