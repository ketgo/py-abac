"""
    Numeric condition base class
"""

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, ConditionCreationError


class NumericCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, value):
        if not is_number(value):
            raise ConditionCreationError("Invalid argument type '{}' for numeric condition.".format(type(value)))
        self.value = value


def is_number(value):
    return isinstance(value, float) or isinstance(value, int)


class NumericConditionSchema(Schema):
    value = fields.Number(required=True, allow_none=False)
