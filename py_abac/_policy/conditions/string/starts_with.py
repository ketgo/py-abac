"""
    String starts with conditions
"""

from marshmallow import post_load

from .base import StringCondition


class StartsWith(StringCondition):
    """
        Condition for string `what` starts with `value`
    """
    # Condition type specifier
    condition: str = "StartsWith"

    def _is_satisfied(self, what) -> bool:
        if self.case_insensitive:
            return what.lower().startswith(self.value.lower())
        return what.startswith(self.value)
