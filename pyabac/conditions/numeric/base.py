"""
    Numeric condition base class
"""

import logging

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, abstractmethod

log = logging.getLogger(__name__)


def is_number(value):
    return isinstance(value, float) or isinstance(value, int)


class NumericCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx):
        if not is_number(ctx.attribute_value):
            log.debug("Invalid type '{}' for attribute value at path '{}' for element '{}'. "
                      "Condition not satisfied.".format(ctx.attribute_value, ctx.attribute_path, ctx.ace))
            return False
        return self._is_satisfied(ctx.attribute_value)

    @abstractmethod
    def _is_satisfied(self, what):
        """
            Is numeric condition satisfied

            :param what: numeric value to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class NumericConditionSchema(Schema):
    value = fields.Number(required=True, allow_none=False)
