"""
    Numeric less than conditions
"""

from .base import NumericCondition


class Lt(NumericCondition):
    """
        Condition for number `what` less than `value`
    """
    # Condition type specifier
    condition: str = "Lt"

    def _is_satisfied(self, what) -> bool:
        return what < self.value
