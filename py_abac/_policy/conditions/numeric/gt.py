"""
    Numeric greater than conditions
"""

from .base import NumericCondition


class Gt(NumericCondition):
    """
        Condition for number `what` greater than `value`
    """
    # Condition type specifier
    condition: str = "Gt"

    def _is_satisfied(self, what) -> bool:
        return what > self.value
