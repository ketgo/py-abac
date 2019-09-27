"""
    String regex match condition
"""

import re

from marshmallow import Schema, fields, post_load

from .base import ConditionBase, ConditionCreationError, is_string


class RegexMatch(ConditionBase):

    def __init__(self, value):
        if not is_regex(value):
            raise ConditionCreationError("Argument '{}' not a valid regexp string.".format(value))
        self.value = value

    def is_satisfied(self, what):
        if not is_string(what):
            return False
        return re.search(self.value, what) is not None


def is_regex(value):
    # noinspection PyBroadException
    try:
        re.compile(value)
    except Exception:
        return False
    return True


class RegexMatchSchema(Schema):
    value = fields.String(required=True, allow_none=False)

    @post_load
    def post_load(self, data, **_):
        return RegexMatch(**data)
