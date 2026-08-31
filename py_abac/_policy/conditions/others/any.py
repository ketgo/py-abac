"""
    Attribute any value conditions
"""
from marshmallow import Schema, post_load

from ..base import ConditionBase


class Any(ConditionBase):
    """
        Condition for attribute having any value
    """
    # Condition type specifier
    condition: str = "Any"

    def is_satisfied(self, ctx) -> bool:
        return True
