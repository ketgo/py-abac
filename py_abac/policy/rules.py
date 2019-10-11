"""
    Policy rules class
"""

from marshmallow import Schema, fields, post_load

from .conditions.others.equals_attribute import validate_path
from .conditions.schema import ConditionSchema
from ..context import EvaluationContext


class Rules(object):

    def __init__(self, subject, resource, action, context):
        self.subject = subject
        self.resource = resource
        self.action = action
        self.context = context

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

        # If ace is not in correct format, return False. This condition is just for best practice and will never happen
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


class RuleField(fields.Field):
    """
        Marshmallow field class for rules
    """
    _implicit_and_field = fields.Dict(keys=fields.String(validate=validate_path),
                                      values=fields.Nested(ConditionSchema))
    _implicit_or_field = fields.List(fields.Dict(keys=fields.String(validate=validate_path),
                                                 values=fields.Nested(ConditionSchema)))

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, list):
            return self._implicit_or_field._serialize(value, attr, obj, **kwargs)
        return self._implicit_and_field._serialize(value, attr, obj, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list):
            return self._implicit_or_field._deserialize(value, attr, data, **kwargs)
        return self._implicit_and_field._deserialize(value, attr, data, **kwargs)


class RulesSchema(Schema):
    subject = RuleField(default={}, missing={})
    resource = RuleField(default={}, missing={})
    action = RuleField(default={}, missing={})
    context = RuleField(default={}, missing={})

    @post_load
    def post_load(self, data, **_):
        return Rules(**data)
