"""
    Any of the values in collection conditions
"""

from .base import CollectionCondition


class AnyIn(CollectionCondition):
    """
        Condition for any value of `what` in `values`
    """
    # Condition type specifier
    condition: str = "AnyIn"

    def _is_satisfied(self, what) -> bool:
        return bool(set(what).intersection(self.values))
