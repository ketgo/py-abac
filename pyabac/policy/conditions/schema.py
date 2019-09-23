"""
    Condition one-of schema
"""

from marshmallow import ValidationError
from marshmallow_oneofschema import OneOfSchema

# --- Collection Conditions ---
from .collection.all_in import AllInCondition, AllInConditionSchema
from .collection.all_not_in import AllNotInCondition, AllNotInConditionSchema
from .collection.any_in import AnyInCondition, AnyInConditionSchema
from .collection.any_not_in import AnyNotInCondition, AnyNotInConditionSchema
from .collection.is_empty import IsEmptyCondition, IsEmptyConditionSchema
from .collection.is_in import IsInCondition, IsInConditionSchema
from .collection.is_not_empty import IsNotEmptyCondition, IsNotEmptyConditionSchema
from .collection.is_not_in import IsNotInCondition, IsNotInConditionSchema
# --- Other Conditions ---
from .exists import ExistsCondition, ExistsConditionSchema
from .exists import NotExistsCondition, NotExistsConditionSchema
# --- Logic Conditions ---
from .logic._and import AndCondition, AndConditionSchema
from .logic._not import NotCondition, NotConditionSchema
from .logic._or import OrCondition, OrConditionSchema
# --- Network Conditions ---
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
        IsEmptyCondition.name: IsEmptyConditionSchema,
        IsNotEmptyCondition.name: IsNotEmptyConditionSchema,
        # --- Logic Conditions ---
        AndCondition.name: AndConditionSchema,
        OrCondition.name: OrConditionSchema,
        NotCondition.name: NotConditionSchema,
        # --- Network Conditions ---
        CIDRCondition.name: CIDRConditionSchema,
        # --- Other Conditions ---
        ExistsCondition.name: ExistsConditionSchema,
        NotExistsCondition.name: NotExistsConditionSchema,
    }

    def get_obj_type(self, obj):
        try:
            return getattr(obj, "name")
        except AttributeError:  # pragma: no cover
            raise ValidationError("Unknown condition {} found.".format(obj))  # pragma: no cover
