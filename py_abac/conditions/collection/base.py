"""
    Collection condition base class
"""

import logging

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, abstractmethod

log = logging.getLogger(__name__)


def is_collection(value):
    return any([isinstance(value, list), isinstance(value, set), isinstance(value, tuple)])


class CollectionCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx):
        if not is_collection(ctx.attribute_value):
            log.debug("Invalid type '{}' for attribute value at path '{}' for element '{}'. "
                      "Condition not satisfied.".format(ctx.attribute_value, ctx.attribute_path, ctx.ace))
            return False
        return self._is_satisfied(ctx.attribute_value)

    @abstractmethod
    def _is_satisfied(self, what):
        """
            Is collection condition satisfied

            :param what: collection to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class CollectionConditionSchema(Schema):
    value = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)
