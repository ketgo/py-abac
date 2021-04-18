"""
    String equals conditions
"""

from marshmallow import post_load

from .base import StringCondition


class Equals(StringCondition):
    """
        Condition for string `what` equals `value`
    """
    # Condition type specifier
    condition: str = "Equals"

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower() == self.value.lower()
        return what == self.value
