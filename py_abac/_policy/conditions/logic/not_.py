"""
    Logical NOT conditions
"""

from typing import Any

from .base import ConditionBase


class Not(ConditionBase):
    """
        Condition for logical NOT condition
    """
    # Condition type specifier
    condition: str = "Not"
    value: Any

    def is_satisfied(self, ctx) -> bool:
        return not self.value.is_satisfied(ctx)
