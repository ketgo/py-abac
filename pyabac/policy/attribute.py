"""
    Inquiry element-attribute condition
"""

from marshmallow import fields

from policy.conditions.base import ConditionBase, ConditionCreationError
from policy.conditions.schema import ConditionSchema


def is_path(path):
    return isinstance(path, str)


def is_condition(condition):
    return isinstance(condition, ConditionBase)


class Attribute(ConditionBase):
    """
        Class implementing a policy for a single attribute an inquiry element.
    """

    def __init__(self, path: str, condition: ConditionBase):
        """
            Initialize element policy

            :param path: path to attribute in an inquiry element
            :param condition: rule to check for the attribute
        """
        if not isinstance(path, str):
            raise ConditionCreationError("Invalid type '{}' for attribute path.")
        self.path = path
        if not isinstance(condition, ConditionBase):
            raise ConditionCreationError("Invalid type '{}' for attribute condition.")
        self.condition = condition

    def is_satisfied(self, what):
        raise NotImplementedError()

    def to_json(self):
        pass

    @staticmethod
    def from_json(data):
        pass


class AttributeField(fields.Mapping):
    """
        Attribute field used for marshalling
    """

    def __init__(self, **kwargs):
        super().__init__(keys=fields.String(required=True, allow_none=False),
                         values=fields.Nested(ConditionSchema(), required=True, allow_none=False), **kwargs)
