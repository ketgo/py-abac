"""
    Collection condition base class
"""

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, ConditionCreationError


def is_collection(value):
    return any([isinstance(value, list), isinstance(value, set), isinstance(value, tuple)])


class CollectionCondition(ConditionBase, metaclass=ABCMeta):

    def __init__(self, value):
        if not is_collection(value):
            raise ConditionCreationError("Invalid argument type '{}' for collection condition.".format(type(value)))
        self.value = value


class CollectionConditionSchema(Schema):
    value = fields.List(fields.Raw(required=True, allow_none=False), required=True, allow_none=False)
