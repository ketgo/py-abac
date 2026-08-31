"""
    Logical OR conditions
"""

from .base import LogicCondition


class AnyOf(LogicCondition):
    """
        Condition for any of sub-rules are satisfied
    """
    # Condition type specifier
    condition: str = "AnyOf"

    def is_satisfied(self, ctx) -> bool:
        return any(value.is_satisfied(ctx) for value in self.values)
