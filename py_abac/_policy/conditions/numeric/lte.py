"""
    Numeric less than equal conditions
"""

from .base import NumericCondition


class Lte(NumericCondition):
    """
        Condition for number `what` less than equals `value`
    """
    # Condition type specifier
    condition: str = "Lte"

    def _is_satisfied(self, what) -> bool:
        return what <= self.value
