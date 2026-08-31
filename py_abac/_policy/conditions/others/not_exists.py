"""
    Attribute does not exists conditions
"""

from ..base import ConditionBase


class NotExists(ConditionBase):
    """
        Condition for attribute value not exists
    """
    # Condition type specifier
    condition: str = "NotExists"

    def is_satisfied(self, ctx) -> bool:
        return ctx.attribute_value is None
