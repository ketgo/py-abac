"""
    Attribute Condition Base
"""

from typing import Any

from marshmallow import ValidationError
from objectpath import Tree
from pydantic import PrivateAttr

from ..base import ConditionBase, ABCMeta, abstractmethod


def validate_path(path):
    """
        Validate given attribute path satisfies ObjectPath notation.
        Throws ValidationError for invalid path.
    """
    try:
        Tree({}).execute(path)
    except Exception as err:
        raise ValidationError(*err.args)


class AccessControlElementField(str):
    """
        Access control element field
    """
    # Access control elements
    aces = ["subject", "resource", "action", "context"]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v not in cls.aces:
            raise ValueError("Must be one of: {}".format(cls.aces))
        return v


class ObjectPathField(str):
    """
        ObjectPath field
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            Tree({}).execute(v)
        except Exception:
            raise ValueError("Invalid ObjectPath notation")
        return v


class AttributeCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for attribute conditions
    """
    ace: AccessControlElementField
    path: ObjectPathField
    _value: Any = PrivateAttr()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None

    def is_satisfied(self, ctx) -> bool:
        # Extract attribute value from request to match
        self._value = ctx.get_attribute_value(self.ace, self.path)
        return self._is_satisfied(ctx.attribute_value)

    @abstractmethod
    def _is_satisfied(self, what) -> bool:
        """
            Is attribute conditions satisfied

            :param what: attribute value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()
