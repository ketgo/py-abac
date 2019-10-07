"""
    Policy conditions class
"""

from marshmallow import Schema, fields, post_load
from marshmallow_union import Union

from ..conditions.others.equals_attribute import validate_path
from ..conditions.schema import ConditionSchema
from ..context import EvaluationContext
from ..request import Request


class Conditions(object):

    def __init__(self, subject, resource, action, context):
        self.subject = subject
        self.resource = resource
        self.action = action
        self.context = context

    def is_satisfied(self, request: Request):
        """
            Check if request satisfies all conditions

            :param request: authorization request
            :return: True if satisfied else False
        """
        return self._is_satisfied("subject", self.subject, request) and \
               self._is_satisfied("resource", self.resource, request) and \
               self._is_satisfied("action", self.action, request) and \
               self._is_satisfied("context", self.context, request)

    def _is_satisfied(self, ace_name: str, ace_conditions, request: Request):
        """
            Check if the access control element satisfies request

            :param ace_name: access control element name
            :param ace_conditions: access control element conditions
            :param request: authorization request
            :return: True if satisfied else False
        """
        if isinstance(ace_conditions, list):
            return self._implicit_or(ace_name, ace_conditions, request)
        if isinstance(ace_conditions, dict):
            return self._implicit_and(ace_name, ace_conditions, request)

        # If ace is not in correct format, return False
        return False

    def _implicit_or(self, ace_name: str, ace_conditions: list, request: Request):
        for _ace_conditions in ace_conditions:
            # If even one of the condition is satisfied, return True
            if self._implicit_and(ace_name, _ace_conditions, request):
                return True
        # If no conditions are satisfied, return False
        return False

    @staticmethod
    def _implicit_and(ace_name: str, ace_conditions: dict, request: Request):
        for attribute_path, condition in ace_conditions.items():
            context = EvaluationContext(request)
            context.ace = ace_name
            context.attribute_path = attribute_path
            # If even one of the condition is not satisfied, return False
            if not condition.is_satisfied(context):
                return False
        # If all conditions are satisfied, return True
        return True


ConditionsField = Union([
    fields.Dict(keys=fields.String(validate=validate_path), values=fields.Nested(ConditionSchema), default={},
                missing={}),
    fields.List(fields.Dict(keys=fields.String(validate=validate_path), values=fields.Nested(ConditionSchema)),
                default=[], missing=[])
])


class ConditionsSchema(Schema):
    subject = ConditionsField
    resource = ConditionsField
    action = ConditionsField
    context = ConditionsField

    @post_load
    def post_load(self, data, **_):
        return Conditions(**data)
