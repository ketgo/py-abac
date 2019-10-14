"""
    Equals attribute conditions
"""

from marshmallow import Schema, fields, post_load, validate, ValidationError
from objectpath import Tree

from ..base import ConditionBase


class EqualsAttribute(ConditionBase):
    """
        Equals attribute conditions
    """

    def __init__(self, ace, path):
        self.ace = ace
        self.path = path

    def is_satisfied(self, ctx):
        # Extract attribute value from request and check if it matches that in the context
        return ctx.get_attribute_value(self.ace, self.path) == ctx.attribute_value


def validate_path(path):
    try:
        Tree({}).execute(path)
    except Exception as err:
        raise ValidationError(*err.args)


class EqualsAttributeSchema(Schema):
    ace = fields.String(required=True, validate=validate.OneOf(["subject", "resource", "action", "context"]))
    path = fields.String(required=True, validate=validate_path)

    @post_load
    def post_load(self, data, **_):
        return EqualsAttribute(**data)
