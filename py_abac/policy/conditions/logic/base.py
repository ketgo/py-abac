"""
    Logic conditions base class
"""

from marshmallow import Schema, fields, validate

from ..base import ConditionBase, ABCMeta


class LogicCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for logical conditions
    """

    def __init__(self, values):
        self.values = values

    def is_satisfied(self, ctx) -> bool:
        raise NotImplementedError()


class LogicConditionSchema(Schema):
    """
        Base JSON schema for logical conditions
    """
    values = fields.Nested("ConditionSchema", required=True, allow_none=False, many=True,
                           validate=validate.Length(min=1))
