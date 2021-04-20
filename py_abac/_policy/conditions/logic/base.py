"""
    Logic conditions base class
"""

from typing import List

from ..base import ConditionBase, ABCMeta


class LogicCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for logical conditions
    """
    values: List

    def is_satisfied(self, ctx) -> bool:
        raise NotImplementedError()
