"""
    Not equals attribute condition
"""

from .base import AttributeCondition


class NotEqualsAttribute(AttributeCondition):
    """
        Condition for attribute value not equals that of another
    """
    # Condition type specifier
    condition: str = "NotEqualsAttribute"

    def _is_satisfied(self, what) -> bool:
        return what != self._value
