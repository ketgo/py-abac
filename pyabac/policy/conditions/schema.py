"""
    Condition one-of schema
"""

from marshmallow import ValidationError
from marshmallow_oneofschema import OneOfSchema

from .numeric.eq import EqualCondition, EqualConditionSchema
from .numeric.gt import GreaterCondition, GreaterConditionSchema
from .numeric.gte import GreaterEqualCondition, GreaterEqualConditionSchema
from .numeric.lt import LessCondition, LessConditionSchema
from .numeric.lte import LessEqualCondition, LessEqualConditionSchema


class ConditionSchema(OneOfSchema):
    type_field = "condition"
    type_schemas = {
        EqualCondition.name: EqualConditionSchema,
        GreaterCondition.name: GreaterConditionSchema,
        LessCondition.name: LessConditionSchema,
        GreaterEqualCondition.name: GreaterEqualConditionSchema,
        LessEqualCondition.name: LessEqualConditionSchema,
    }

    def get_obj_type(self, obj):
        try:
            return getattr(obj, "name")
        except AttributeError:
            raise ValidationError("Unknown condition {} found.".format(obj))
