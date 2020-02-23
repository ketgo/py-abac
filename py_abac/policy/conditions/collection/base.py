"""
    Collection conditions base class
"""

import logging

from marshmallow import Schema, fields

from ..base import ConditionBase, ABCMeta, abstractmethod

LOG = logging.getLogger(__name__)


def is_collection(value):
    """
        Check if value is a collection
    """
    return any([isinstance(value, list), isinstance(value, set), isinstance(value, tuple)])


class CollectionCondition(ConditionBase, metaclass=ABCMeta):
    """
        Base class for collection conditions

        :param values: collection of values to compare during policy evaluation
    """

    def __init__(self, values):
        self.values = values

    def is_satisfied(self, ctx):
        if not is_collection(ctx.attribute_value):
            LOG.debug(
                "Invalid type '%s' for attribute value at path '%s' for element '%s'."
                " Condition not satisfied.",
                type(ctx.attribute_value),
                ctx.attribute_path,
                ctx.ace
            )
            return False
        return self._is_satisfied(ctx.attribute_value)

    @abstractmethod
    def _is_satisfied(self, what):
        """
            Is collection conditions satisfied

            :param what: collection to check
            :return: True if satisfied else False
        """
        raise NotImplementedError()


class CollectionConditionSchema(Schema):
    """
        Base JSON schema class for collection conditions
    """
    values = fields.List(
        fields.Raw(required=True, allow_none=False),
        required=True,
        allow_none=False
    )
