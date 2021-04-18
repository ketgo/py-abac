"""
    Policy rules class
"""

from typing import Union, List, Dict

from pydantic import BaseModel

from .conditions.schema import ConditionSchema as Condition
from ..context import EvaluationContext


class ObjectPathField:
    """
        ObjectPath field
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("str type in ObjectPath notion expected")
        return v


class Rules(BaseModel):
    """
        Policy rules
    """
    subject: Union[
        Dict[ObjectPathField, Condition],
        List[Dict[ObjectPathField, Condition]]
    ]
    resource: Union[
        Dict[ObjectPathField, Condition],
        List[Dict[ObjectPathField, Condition]]
    ]
    action: Union[
        Dict[ObjectPathField, Condition],
        List[Dict[ObjectPathField, Condition]]
    ]
    context: Union[
        Dict[ObjectPathField, Condition],
        List[Dict[ObjectPathField, Condition]]
    ]

    def is_satisfied(self, ctx: EvaluationContext):
        """
            Check if request satisfies all conditions

            :param ctx: policy evaluation context
            :return: True if satisfied else False
        """
        return self._is_satisfied("subject", self.subject, ctx) and \
               self._is_satisfied("resource", self.resource, ctx) and \
               self._is_satisfied("action", self.action, ctx) and \
               self._is_satisfied("context", self.context, ctx)

    def _is_satisfied(self, ace_name: str, ace_conditions, ctx: EvaluationContext):
        """
            Check if the access control element satisfies request

            :param ace_name: access control element name
            :param ace_conditions: access control element conditions
            :param ctx: policy evaluation context
            :return: True if satisfied else False
        """
        if isinstance(ace_conditions, list):
            return self._implicit_or(ace_name, ace_conditions, ctx)
        if isinstance(ace_conditions, dict):
            return self._implicit_and(ace_name, ace_conditions, ctx)

        # If ace is not in correct format, return False. This condition is just for best
        # practice and will never happen
        return False  # pragma: no cover

    def _implicit_or(self, ace_name: str, ace_conditions: list, ctx: EvaluationContext):
        for _ace_conditions in ace_conditions:
            # If even one of the conditions is satisfied, return True
            if self._implicit_and(ace_name, _ace_conditions, ctx):
                return True
        # If no conditions are satisfied, return False
        return False

    @staticmethod
    def _implicit_and(ace_name: str, ace_conditions: dict, ctx: EvaluationContext):
        for attribute_path, condition in ace_conditions.items():
            ctx.ace = ace_name
            ctx.attribute_path = attribute_path
            # If even one of the conditions is not satisfied, return False
            if not condition.is_satisfied(ctx):
                return False
        # If all conditions are satisfied, return True
        return True
