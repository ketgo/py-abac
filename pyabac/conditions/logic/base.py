"""
    Logic condition base class
"""

from marshmallow import Schema, fields, validate

from ..base import ConditionBase, ABCMeta


class LogicCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, values):
        self.values = values


class LogicConditionSchema(Schema):
    values = fields.Nested("ConditionSchema", required=True, allow_none=False, many=True,
                           validate=validate.Length(min=1))
