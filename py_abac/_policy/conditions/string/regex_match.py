"""
    String regex match conditions
"""

import re

from marshmallow import Schema, fields, post_load, ValidationError

from .base import StringCondition


class RegexMatch(StringCondition):
    """
        Condition for string `what` matches regex `value`
    """

    def _is_satisfied(self, what) -> bool:
        return re.search(self.value, what) is not None


def validate_regex(value):
    """
        Validate given regex. Throws ValidationError exception
        for invalid regex expressions.
    """
    # noinspection PyBroadException
    try:
        re.compile(value)
    except Exception:
        raise ValidationError("Invalid regex expression '{}'.".format(value))


class RegexMatchSchema(Schema):
    """
        JSON schema for regex match string condition
    """
    value = fields.String(required=True, allow_none=False, validate=validate_regex)

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return RegexMatch(**data)
