"""
    String conditions base class
"""

import logging

from pydantic import StrictStr

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
    value: StrictStr
    case_insensitive: bool = False

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
