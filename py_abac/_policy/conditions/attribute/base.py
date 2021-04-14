"""
    Attribute Condition Base
"""

from marshmallow import Schema, fields, validate, ValidationError
from objectpath import Tree

from ..base import ConditionBase, ABCMeta, abstractmethod


class AttributeCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for attribute conditions

        :param ace: access control element type
        :param path: path to the attribute of the access control element
    """

    def __init__(self, ace, path):
        self.ace = ace
        self.path = path
        self.value = None

    def is_satisfied(self, ctx) -> bool:
        # Extract attribute value from request to match
        self.value = ctx.get_attribute_value(self.ace, self.path)
        return self._is_satisfied(ctx.attribute_value)

    @abstractmethod
    def _is_satisfied(self, what) -> bool:
        """
            Is attribute conditions satisfied

            :param what: attribute value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


def validate_path(path):
    """
        Validate given attribute path satisfies ObjectPath notation.
        Throws ValidationError for invalid path.
    """
    try:
        Tree({}).execute(path)
    except Exception as err:
        raise ValidationError(*err.args)


class AttributeConditionSchema(Schema):
    """
        Base JSON schema for attribute condition
    """
    ace = fields.String(
        required=True,
        validate=validate.OneOf(["subject", "resource", "action", "context"])
    )
    path = fields.String(
        required=True,
        validate=validate_path
    )
