"""
    Operation base class
"""

from abc import ABCMeta, abstractmethod

from marshmallow import ValidationError

from pyabac.common.exceptions import ConditionCreationError


class ConditionBase(metaclass=ABCMeta):

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
        return ConditionSchema().dump(self)

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
