"""
    Conditions relevant to networking context
"""

import ipaddress
import logging

from marshmallow import Schema, fields, post_load

from ..base import ConditionBase

LOG = logging.getLogger(__name__)


class CIDR(ConditionBase):
    """
        Condition for IP address `what` in CIDR `value`.
    """

    def __init__(self, value):
        self.value = value

    def is_satisfied(self, ctx) -> bool:
        if not isinstance(ctx.attribute_value, str):
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
        """
            Is CIDR conditions satisfied

            :param what: IP address to check
            :return: True if satisfied else False
        """
        try:
            ip_addr = ipaddress.ip_address(what)
            net = ipaddress.ip_network(self.value)
        except ValueError:
            return False
        return ip_addr in net


class CIDRSchema(Schema):
    """
        JSON schema for CIDR condition
    """
    value = fields.String(required=True, allow_none=False)

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        return CIDR(**data)
