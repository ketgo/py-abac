"""
    Numeric equal conditions
"""

from .base import NumericCondition


class Eq(NumericCondition):
    """
        Condition for number `what` equals `value`
    """
    # Condition type specifier
    condition: str = "Eq"

    def _is_satisfied(self, what) -> bool:
        return what == self.value
