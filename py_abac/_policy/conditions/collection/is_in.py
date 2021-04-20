"""
    Value is in collection conditions
"""

from .base import CollectionCondition


class IsIn(CollectionCondition):
    """
        Condition for `what` is a member of `values`
    """
    # Condition type specifier
    condition: str = "IsIn"

    def is_satisfied(self, ctx):
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what) -> bool:
        return what in self.values
