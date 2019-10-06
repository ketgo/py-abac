"""
    Numeric condition base class
"""

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, abstractmethod


def is_number(value):
    return isinstance(value, float) or isinstance(value, int)


class NumericCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx):
        return self._is_satisfied(ctx.attribute_value)

    @abstractmethod
    def _is_satisfied(self, value):
        """
            Is numeric condition satisfied

            :param value: numeric value
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class NumericConditionSchema(Schema):
    value = fields.Number(required=True, allow_none=False)
