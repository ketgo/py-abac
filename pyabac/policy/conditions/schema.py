"""
    Condition one-of schema
"""

from marshmallow import ValidationError
from marshmallow_oneofschema import OneOfSchema

from .collection.all_in import AllInCondition, AllInConditionSchema
from .collection.all_not_in import AllNotInCondition, AllNotInConditionSchema
from .collection.any_in import AnyInCondition, AnyInConditionSchema
from .collection.any_not_in import AnyNotInCondition, AnyNotInConditionSchema
# --- Collection Conditions ---
from .collection.is_in import IsInCondition, IsInConditionSchema
from .collection.is_not_in import IsNotInCondition, IsNotInConditionSchema
# --- Logic Conditions ---
from .logic._all import AllCondition, AllConditionSchema
from .logic._any import AnyCondition, AnyConditionSchema
from .logic._not import NotCondition, NotConditionSchema
# -- Network Conditions --
from .net import CIDRCondition, CIDRConditionSchema
# --- Numeric Conditions ---
from .numeric.eq import EqualCondition, EqualConditionSchema
from .numeric.gt import GreaterCondition, GreaterConditionSchema
from .numeric.gte import GreaterEqualCondition, GreaterEqualConditionSchema
from .numeric.lt import LessCondition, LessConditionSchema
from .numeric.lte import LessEqualCondition, LessEqualConditionSchema
from .numeric.neq import NotEqualCondition, NotEqualConditionSchema
# --- String Conditions ---
from .string.contains import ContainsCondition, ContainsConditionSchema
from .string.ends_with import EndsWithCondition, EndsWithConditionSchema
from .string.equals import EqualsCondition, EqualsConditionSchema
from .string.not_contains import NotContainsCondition, NotContainsConditionSchema
from .string.not_equals import NotEqualsCondition, NotEqualsConditionSchema
from .string.regex_match import RegexMatchCondition, RegexMatchConditionSchema
from .string.starts_with import StartsWithCondition, StartsWithConditionSchema


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
        # --- Collection Conditions ---
        IsInCondition.name: IsInConditionSchema,
        IsNotInCondition.name: IsNotInConditionSchema,
        AllInCondition.name: AllInConditionSchema,
        AllNotInCondition.name: AllNotInConditionSchema,
        AnyInCondition.name: AnyInConditionSchema,
        AnyNotInCondition.name: AnyNotInConditionSchema,
        # --- Logic Conditions ---
        AllCondition.name: AllConditionSchema,
        AnyCondition.name: AnyConditionSchema,
        NotCondition.name: NotConditionSchema,
        # -- Network Conditions --
        CIDRCondition.name: CIDRConditionSchema,
    }

    def get_obj_type(self, obj):
        try:
            return getattr(obj, "name")
        except AttributeError:
            raise ValidationError("Unknown condition {} found.".format(obj))
