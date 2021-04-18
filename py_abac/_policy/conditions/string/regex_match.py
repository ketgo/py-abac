"""
    String regex match conditions
"""

import re

from .base import ConditionBase, LOG, is_string
from pydantic import validator, ValidationError


class RegexMatch(ConditionBase):
    """
        Condition for string `what` matches regex `value`
    """
    # Condition type specifier
    condition: str = "RegexMatch"
    value: str

    @validator('value')
    def is_regex(cls, v):
        validate_regex(v)
        return v

    def is_satisfied(self, ctx) -> bool:
        if not is_string(ctx.attribute_value):
            LOG.debug(
                "Invalid type '%s' for attribute value at path '%s' for element '%s'."
                " Condition not satisfied.",
                type(ctx.attribute_value),
                ctx.attribute_path,
                ctx.ace
            )
            return False
        return self._is_satisfied(ctx.attribute_value)

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
