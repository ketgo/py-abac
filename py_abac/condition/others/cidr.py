"""
    Conditions relevant to networking context
"""

import ipaddress
import logging

from marshmallow import Schema, fields, post_load

from ..base import ConditionBase

log = logging.getLogger(__name__)


def is_cidr(value):
    return isinstance(value, str)


class CIDR(ConditionBase):
    """
        Condition that is satisfied when inquiry's IP address is in the provided CIDR.
    """

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx):
        if not isinstance(ctx.attribute_value, str):
            log.debug("Invalid type '{}' for attribute value at path '{}' for element '{}'. "
                      "Condition not satisfied.".format(ctx.attribute_value, ctx.attribute_path, ctx.ace))
            return False
        return self._is_satisfied(ctx.attribute_value)

    def _is_satisfied(self, what):
        try:
            ip = ipaddress.ip_address(what)
            net = ipaddress.ip_network(self.value)
        except ValueError:
            return False
        return ip in net


class CIDRSchema(Schema):
    value = fields.String(required=True, allow_none=False)

    @post_load
    def post_load(self, data, **_):
        return CIDR(**data)
