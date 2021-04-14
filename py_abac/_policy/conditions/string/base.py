"""
    String conditions base class
"""

import logging

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


def is_string(value) -> bool:
    """
        Check if value is string
    """
    return isinstance(value, str)


class StringCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for string conditions
    """

    def __init__(self, value, case_insensitive=False):
        self.case_insensitive = case_insensitive or False
        self.value = value

    def is_satisfied(self, ctx) -> bool:
        if not is_string(ctx.attribute_value):
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
            Is string conditions satisfied

            :param what: string value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class StringConditionSchema(Schema):
    """
        Base JSON schema for string conditions
    """
    value = fields.String(required=True, allow_none=False)
    case_insensitive = fields.Bool(default=False, missing=False)
