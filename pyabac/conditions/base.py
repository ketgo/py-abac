"""
    Operation base class
"""

from abc import ABCMeta, abstractmethod


class ConditionBase(metaclass=ABCMeta):

    @abstractmethod
    def is_satisfied(self, ctx):
        """
            Is condition satisfied?

            :param ctx: evaluation context
            :return: True if satisfied else False
        """
        raise NotImplementedError()
