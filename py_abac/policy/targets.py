"""
    Policy targets class
"""

import fnmatch

from marshmallow import Schema, fields, post_load, validate

from ..context import EvaluationContext


class Targets(object):
    """
        Policy targets
    """

    def __init__(self, subject_id: list, resource_id: list, action_id: list):
        self.subject_id = subject_id
        self.resource_id = resource_id
        self.action_id = action_id

    def match(self, ctx: EvaluationContext):
        """
            Check if request matches policy targets

            :param ctx: policy evaluation context
            :return: True if matches else False
        """
        return self._is_in(self.subject_id, ctx.subject_id) and \
               self._is_in(self.resource_id, ctx.resource_id) and \
               self._is_in(self.action_id, ctx.action_id)

    @staticmethod
    def _is_in(ace_ids, ace_id: str):
        """
            Returns True if `ace_id` is in `ace_ids`.
        """
        _ace_ids = ace_ids if isinstance(ace_ids, list) else [ace_ids]
        for _id in _ace_ids:
            # Unix file name type string matching
            if fnmatch.fnmatch(ace_id, _id):
                return True
        return False


class TargetField(fields.Field):
    """
        Marshmallow field class for targets
    """
    _single = fields.String(validate=validate.Length(min=1))
    _many = fields.List(
        fields.String(validate=validate.Length(min=1)),
        validate=validate.Length(min=1)
    )

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, list):
            return self._many._serialize(value, attr, obj, **kwargs)  # pylint: disable=protected-access
        return self._single._serialize(value, attr, obj, **kwargs)  # pylint: disable=protected-access

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list):
            return self._many._deserialize(value, attr, data, **kwargs)  # pylint: disable=protected-access
        return self._single._deserialize(value, attr, data, **kwargs)  # pylint: disable=protected-access


class TargetsSchema(Schema):
    """
        JSON schema for targets
    """
    subject_id = TargetField(missing="*", default="*")
    resource_id = TargetField(missing="*", default="*")
    action_id = TargetField(missing="*", default="*")

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return Targets(**data)
