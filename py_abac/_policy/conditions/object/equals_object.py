"""
    Equals object conditions
"""

from typing import Dict

from ..base import ConditionBase


class EqualsObject(ConditionBase):
    """
        Equals object conditions
    """
    # Condition type specifier
    condition: str = "EqualsObject"
    value: Dict

    def is_satisfied(self, ctx) -> bool:
        return self.value == ctx.attribute_value
