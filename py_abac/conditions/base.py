"""
    Operation base class
"""

from abc import ABCMeta, abstractmethod

from ..context import EvaluationContext


class ConditionBase(metaclass=ABCMeta):

    @abstractmethod
    def is_satisfied(self, ctx: EvaluationContext):
        """
            Is condition satisfied?

            :param ctx: evaluation context
            :return: True if satisfied else False
        """
        raise NotImplementedError()
