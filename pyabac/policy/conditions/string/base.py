"""
    String condition base class
"""

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta


class StringCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, value, case_insensitive=False):
        if not is_string(value):
            raise TypeError("Invalid argument type '{}' for string condition.".format(type(value)))
        self.case_insensitive = case_insensitive or False
        self.value = value


def is_string(value):
    return isinstance(value, str)


class StringConditionSchema(Schema):
    value = fields.String(required=True, allow_none=False)
    case_insensitive = fields.Bool(default=False, missing=False)
