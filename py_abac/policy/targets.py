"""
    Policy targets class
"""

import fnmatch

from marshmallow import Schema, fields, post_load, validate
from marshmallow_union import Union

from .context import EvaluationContext


class Targets(object):

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
        return self._is_in(self.subject_id, ctx.request.subject_id) and \
               self._is_in(self.resource_id, ctx.request.resource_id) and \
               self._is_in(self.action_id, ctx.request.action_id)

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


TargetsField = Union([
    fields.String(validate=validate.Length(min=1), missing="*", default="*"),
    fields.List(fields.String(validate=validate.Length(min=1)), missing=["*"], default=["*"])
])


class TargetsSchema(Schema):
    subject_id = TargetsField
    resource_id = TargetsField
    action_id = TargetsField

    @post_load
    def post_load(self, data, **_):
        return Targets(**data)
