"""
    Equals attribute condition
"""

from marshmallow import post_load

from .base import AttributeCondition, AttributeConditionSchema


class EqualsAttribute(AttributeCondition):
    """
        Condition for attribute value equals that of another
    """

    def _is_satisfied(self, what) -> bool:
        return what == self.value


class EqualsAttributeSchema(AttributeConditionSchema):
    """
        JSON schema for equals attribute condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return EqualsAttribute(**data)
