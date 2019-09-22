"""
    Operation base class
"""

from abc import ABCMeta, abstractmethod, abstractproperty

from marshmallow import ValidationError

from ...exceptions import ConditionCreationError


class ConditionBase(metaclass=ABCMeta):

    @abstractproperty
    def name(self):
        """
            Name of the condition
        """

    @abstractmethod
    def is_satisfied(self, what):
        """
            Is condition satisfied for the given value `what`

            :param what: value for which to check condition
            :return: bool
        """

    def to_json(self):
        """
            Marshal to JSON

            :return: JSON dict
        """
        from .schema import ConditionSchema
        try:
            return ConditionSchema().dump(self)
        except ValidationError as err:
            raise ConditionCreationError(*err.args)

    @staticmethod
    def from_json(data):
        """
            Marshal from JSON

            :param data: JSON data
            :return: Class instance
        """
        from .schema import ConditionSchema
        try:
            return ConditionSchema().load(data)
        except ValidationError as err:
            raise ConditionCreationError(*err.args)
