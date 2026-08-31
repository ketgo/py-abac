"""
    Numeric greater than equal conditions
"""

from .base import NumericCondition


class Gte(NumericCondition):
    """
        Condition for number `what` greater than equals `value`
    """
    # Condition type specifier
    condition: str = "Gte"

    def _is_satisfied(self, what) -> bool:
        return what >= self.value
