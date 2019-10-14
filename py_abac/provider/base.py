"""
    Attribute provider base class
"""

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..context import EvaluationContext  # pragma: no cover


class AttributeProvider(metaclass=ABCMeta):
    """
        Attribute provider interface
    """

    @abstractmethod
    def get_attribute_value(self, ace: str, attribute_path: str, ctx: 'EvaluationContext'):
        """
            Get attribute value for given access control element and attribute path. If
            attribute not found then returns None.

            :param ace: Access control element
            :param attribute_path: attribute path in ObjectPath format
            :param ctx: evaluation context
            :return: attribute value
        """
        raise NotImplementedError()
