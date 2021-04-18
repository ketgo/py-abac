"""
    String contains conditions
"""

from .base import StringCondition


class Contains(StringCondition):
    """
        Condition for string `what` contains `value`
    """
    # Condition type specifier
    condition: str = "Contains"

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return self.value.lower() in what.lower()
        return self.value in what
