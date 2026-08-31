"""
    Attribute exists conditions
"""

from ..base import ConditionBase


class Exists(ConditionBase):
    """
        Condition for attribute value exists
    """
    # Condition type specifier
    condition: str = "Exists"

    def is_satisfied(self, ctx) -> bool:
        return ctx.attribute_value is not None
