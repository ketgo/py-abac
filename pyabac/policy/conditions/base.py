"""
    Operation base class
"""

from abc import ABCMeta, abstractmethod, abstractproperty


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
        return ConditionSchema().dump(self)

    @staticmethod
    def from_json(data):
        """
            Marshal from JSON

            :param data: JSON data
            :return: Class instance
        """
        from .schema import ConditionSchema
        return ConditionSchema().load(data)
