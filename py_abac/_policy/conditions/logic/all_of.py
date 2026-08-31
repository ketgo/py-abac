"""
    Logical AND conditions
"""

from .base import LogicCondition


class AllOf(LogicCondition):
    """
        Condition for all of the sub-rules are satisfied
    """
    # Condition type specifier
    condition: str = "AllOf"

    def is_satisfied(self, ctx) -> bool:
        return all(value.is_satisfied(ctx) for value in self.values)
