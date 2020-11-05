"""
    Not equals attribute condition
"""

from marshmallow import post_load

from .base import AttributeCondition, AttributeConditionSchema


class NotEqualsAttribute(AttributeCondition):
    """
        Condition for attribute value not equals that of another
    """

    def _is_satisfied(self, what) -> bool:
        return what != self.value


class NotEqualsAttributeSchema(AttributeConditionSchema):
    """
        JSON schema for not equals attribute condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return NotEqualsAttribute(**data)
