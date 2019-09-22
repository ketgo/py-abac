"""
    Logic condition base class
"""

from marshmallow import Schema, fields, validate

from ..base import ConditionBase, ABCMeta, ConditionCreationError


class LogicCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, *values):
        for value in values:
            if not is_condition(value):
                raise ConditionCreationError("Invalid argument type '{}' for logic condition.".format(type(value)))
        self.values = values


def is_condition(value):
    return isinstance(value, ConditionBase)


class LogicConditionSchema(Schema):
    values = fields.Nested("ConditionSchema", required=True, allow_none=False, many=True,
                           validate=validate.Length(min=1, error='May not be an empty list'))
