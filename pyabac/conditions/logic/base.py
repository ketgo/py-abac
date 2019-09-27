"""
    Logic condition base class
"""

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, ConditionCreationError


def is_condition(value):
    return isinstance(value, ConditionBase)


class LogicCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, *values):
        if not values:
            raise ConditionCreationError("No arguments provided in Logic condition.")
        for value in values:
            if not is_condition(value):
                raise ConditionCreationError("Invalid argument type '{}' for logic condition.".format(type(value)))
        self.values = values


class LogicConditionSchema(Schema):
    values = fields.Nested("ConditionSchema", required=True, allow_none=False, many=True)
