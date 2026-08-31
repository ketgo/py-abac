"""
    All of the values in collection conditions
"""

from .base import CollectionCondition


class AllIn(CollectionCondition):
    """
        Condition for all values of `what` in `values`
    """
    # Condition type specifier
    condition: str = "AllIn"

    def _is_satisfied(self, what) -> bool:
        return set(what).issubset(self.values)
