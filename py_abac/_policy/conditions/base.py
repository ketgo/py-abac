"""
    Operation base class
"""

from abc import ABCMeta, abstractmethod

from pydantic import BaseModel

from py_abac.context import EvaluationContext


class ConditionBase(BaseModel, metaclass=ABCMeta):
    """
        Base class for conditions
    """
    # Condition type specifier
    condition: str

    @abstractmethod
    def is_satisfied(self, ctx: EvaluationContext) -> bool:
        """
            Is conditions satisfied?

            :param ctx: evaluation context
            :return: True if satisfied else False
        """
        raise NotImplementedError()
