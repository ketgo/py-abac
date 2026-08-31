"""
    String ends with conditions
"""

from .base import StringCondition


class EndsWith(StringCondition):
    """
        Condition for string `what` ends with `value`
    """
    # Condition type specifier
    condition: str = "EndsWith"

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower().endswith(self.value.lower())
        return what.endswith(self.value)
