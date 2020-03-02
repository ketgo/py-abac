"""
    Equals attribute conditions
"""

from marshmallow import Schema, fields, post_load, validate, ValidationError
from objectpath import Tree

from ..base import ConditionBase


class EqualsAttribute(ConditionBase):
    """
        Condition for attribute value equals that of another
    """

    def __init__(self, ace, path):
        self.ace = ace
        self.path = path

    def is_satisfied(self, ctx) -> bool:
        # Extract attribute value from request and check if it matches that in the context
        return ctx.get_attribute_value(self.ace, self.path) == ctx.attribute_value


def validate_path(path):
    """
        Validate given attribute path satisfies ObjectPath notation.
        Throws ValidationError for invalid path.
    """
    try:
        Tree({}).execute(path)
    except Exception as err:
        raise ValidationError(*err.args)


class EqualsAttributeSchema(Schema):
    """
        JSON schema for equals attribute condition
    """
    ace = fields.String(
        required=True,
        validate=validate.OneOf(["subject", "resource", "action", "context"])
    )
    path = fields.String(
        required=True,
        validate=validate_path
    )

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return EqualsAttribute(**data)
