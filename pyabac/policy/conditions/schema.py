"""
    Condition one-of schema
"""

from marshmallow import ValidationError
from marshmallow_oneofschema import OneOfSchema

# --- Numeric Conditions ---
from .numeric.eq import EqualCondition, EqualConditionSchema
from .numeric.gt import GreaterCondition, GreaterConditionSchema
from .numeric.gte import GreaterEqualCondition, GreaterEqualConditionSchema
from .numeric.lt import LessCondition, LessConditionSchema
from .numeric.lte import LessEqualCondition, LessEqualConditionSchema
from .numeric.neq import NotEqualCondition, NotEqualConditionSchema
# --- String Conditions ---
from .string.contains import ContainsCondition, ContainsConditionSchema
from .string.not_contains import NotContainsCondition, NotContainsConditionSchema
from .string.equals import EqualsCondition, EqualsConditionSchema
from .string.not_equals import NotEqualsCondition, NotEqualsConditionSchema
from .string.starts_with import StartsWithCondition, StartsWithConditionSchema
from .string.ends_with import EndsWithCondition, EndsWithConditionSchema
from .string.regex_match import RegexMatchCondition, RegexMatchConditionSchema


class ConditionSchema(OneOfSchema):
    type_field = "condition"
    type_schemas = {
        # --- Numeric Conditions ---
        EqualCondition.name: EqualConditionSchema,
        GreaterCondition.name: GreaterConditionSchema,
        LessCondition.name: LessConditionSchema,
        GreaterEqualCondition.name: GreaterEqualConditionSchema,
        LessEqualCondition.name: LessEqualConditionSchema,
        NotEqualCondition.name: NotEqualConditionSchema,
        # --- String Conditions ---
        ContainsCondition.name: ContainsConditionSchema,
        NotContainsCondition.name: NotContainsConditionSchema,
        EqualsCondition.name: EqualsConditionSchema,
        NotEqualsCondition.name: NotEqualsConditionSchema,
        StartsWithCondition.name: StartsWithConditionSchema,
        EndsWithCondition.name: EndsWithConditionSchema,
        RegexMatchCondition.name: RegexMatchConditionSchema,
    }

    def get_obj_type(self, obj):
        try:
            return getattr(obj, "name")
        except AttributeError:
            raise ValidationError("Unknown condition {} found.".format(obj))
