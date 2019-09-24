"""
    Logical NOT condition
"""

from marshmallow import Schema, fields, post_load

from .base import ConditionBase, ConditionCreationError, is_condition


class NotCondition(ConditionBase):
    name = "Not"

    def __init__(self, value):
        if not is_condition(value):
            raise ConditionCreationError("Invalid argument type '{}' for logic condition.".format(type(value)))
        self.value = value

    def is_satisfied(self, what):
        return not self.value.is_satisfied(what)


class NotConditionSchema(Schema):
    value = fields.Nested("ConditionSchema", required=True, allow_none=False, many=False)

    @post_load
    def post_load(self, data, **_):
        return NotCondition(**data)
