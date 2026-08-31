"""
    Value is not in collection conditions
"""

from .base import CollectionCondition


class IsNotIn(CollectionCondition):
    """
        Condition for `what` is not a member of `values`
    """
    # Condition type specifier
    condition: str = "IsNotIn"

    def is_satisfied(self, ctx) -> bool:
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what) -> bool:
        return what not in self.values
