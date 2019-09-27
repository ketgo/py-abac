"""
    Conditions relevant to networking context
"""

import ipaddress

from marshmallow import Schema, fields, post_load

from ..base import ConditionBase, ConditionCreationError


def is_cidr(value):
    return isinstance(value, str)


class CIDR(ConditionBase):
    """
        Condition that is satisfied when inquiry's IP address is in the provided CIDR.
    """

    def __init__(self, value):
        if not is_cidr(value):
            raise ConditionCreationError("Invalid argument type '{}' for network condition.".format(type(value)))
        self.value = value

    def is_satisfied(self, what):
        if not isinstance(what, str):
            return False
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
