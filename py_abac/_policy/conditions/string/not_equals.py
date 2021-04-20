"""
    String not equals conditions
"""

from marshmallow import post_load

from .base import StringCondition


class NotEquals(StringCondition):
    """
        Condition for string `what` not equals `value`
    """
    # Condition type specifier
    condition: str = "NotEquals"

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower() != self.value.lower()
        return what != self.value
