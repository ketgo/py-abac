"""
    String regex match condition
"""

import re

from marshmallow import Schema, fields, post_load, ValidationError

from .base import StringCondition


class RegexMatch(StringCondition):

    def _is_satisfied(self, what):
        return re.search(self.value, what) is not None


def validate_regex(value):
    # noinspection PyBroadException
    try:
        re.compile(value)
    except Exception:
        raise ValidationError("Invalid regex expression '{}'.".format(value))


class RegexMatchSchema(Schema):
    value = fields.String(required=True, allow_none=False, validate=validate_regex)

    @post_load
    def post_load(self, data, **_):
        return RegexMatch(**data)
