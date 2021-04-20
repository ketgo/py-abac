"""
    Equals attribute condition
"""

from .base import AttributeCondition


class EqualsAttribute(AttributeCondition):
    """
        Condition for attribute value equals that of another
    """
    # Condition type specifier
    condition: str = "EqualsAttribute"

    def _is_satisfied(self, what) -> bool:
        return what == self._value
