"""
    String not contains conditions
"""

from marshmallow import post_load

from .base import StringCondition


class NotContains(StringCondition):
    """
        Condition for string `what` not contains `value`
    """
    # Condition type specifier
    condition: str = "NotContains"

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return self.value.lower() not in what.lower()
        return self.value not in what
