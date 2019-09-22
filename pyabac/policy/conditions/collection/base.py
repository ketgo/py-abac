"""
    Collection condition base class
"""

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, ConditionCreationError


class CollectionCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, value):
        if not is_collection(value):
            raise ConditionCreationError("Invalid argument type '{}' for collection condition.".format(type(value)))
        self.value = value


def is_collection(value):
    return isinstance(value, list)


class CollectionConditionSchema(Schema):
    value = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)
