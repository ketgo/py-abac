"""
    Any of the values not in collection conditions
"""

from .base import CollectionCondition


class AnyNotIn(CollectionCondition):
    """
        Condition for any values of `what` not in `values`
    """
    # Condition type specifier
    condition: str = "AnyNotIn"

    def _is_satisfied(self, what) -> bool:
        return not bool(set(what).intersection(self.values))
