"""
    All of the values not in collection conditions
"""

from .base import CollectionCondition


class AllNotIn(CollectionCondition):
    """
        Condition for all values of `what` not in `values`
    """
    # Condition type specifier
    condition: str = "AllNotIn"

    def _is_satisfied(self, what) -> bool:
        return not set(what).issubset(self.values)
