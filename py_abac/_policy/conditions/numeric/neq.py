"""
    Numeric not equal conditions
"""

from .base import NumericCondition


class Neq(NumericCondition):
    """
        Condition for number `what` not equals `value`
    """
    # Condition type specifier
    condition: str = "Neq"

    def _is_satisfied(self, what) -> bool:
        return what != self.value
