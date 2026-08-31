"""
    Collection conditions base class
"""

import logging
from typing import Union, List, Set, Tuple

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


def is_collection(value) -> bool:
    """
        Check if value is a collection
    """
    return any([isinstance(value, list), isinstance(value, set), isinstance(value, tuple)])


class CollectionCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for collection conditions
    """
    values: Union[List, Set, Tuple]

    def is_satisfied(self, ctx) -> bool:
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

    @abstractmethod
    def _is_satisfied(self, what) -> bool:
        """
            Is collection conditions satisfied

            :param what: collection to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()
