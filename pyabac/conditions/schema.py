"""
    Condition one-of schema
"""

from marshmallow import ValidationError
from marshmallow_oneofschema import OneOfSchema

# --- Collection Conditions ---
from .collection.all_in import AllIn, AllInSchema
from .collection.all_not_in import AllNotIn, AllNotInSchema
from .collection.any_in import AnyIn, AnyInSchema
from .collection.any_not_in import AnyNotIn, AnyNotInSchema
from .collection.is_empty import IsEmpty, IsEmptySchema
from .collection.is_in import IsIn, IsInSchema
from .collection.is_not_empty import IsNotEmpty, IsNotEmptySchema
from .collection.is_not_in import IsNotIn, IsNotInSchema
# --- Logic Conditions ---
from .logic._and import And, AndSchema
from .logic._not import Not, NotSchema
from .logic._or import Or, OrSchema
# --- Numeric Conditions ---
from .numeric.eq import Eq, EqSchema
from .numeric.gt import Gt, GtSchema
from .numeric.gte import Gte, GteSchema
from .numeric.lt import Lt, LtSchema
from .numeric.lte import Lte, LteSchema
from .numeric.neq import Neq, NeqSchema
# --- Other Conditions ---
from .others.exists import Exists, ExistsSchema
from .others.not_exists import NotExists, NotExistsSchema
from .others.net import CIDR, CIDRSchema
from .others.any import Any, AnySchema
# --- String Conditions ---
from .string.contains import Contains, ContainsSchema
from .string.ends_with import EndsWith, EndsWithSchema
from .string.equals import Equals, EqualsSchema
from .string.not_contains import NotContains, NotContainsSchema
from .string.not_equals import NotEquals, NotEqualsSchema
from .string.regex_match import RegexMatch, RegexMatchSchema
from .string.starts_with import StartsWith, StartsWithSchema


class ConditionSchema(OneOfSchema):
    type_field = "condition"
    type_schemas = {
        # --- Numeric Conditions ---
        Eq.__name__: EqSchema,
        Gt.__name__: GtSchema,
        Lt.__name__: LtSchema,
        Gte.__name__: GteSchema,
        Lte.__name__: LteSchema,
        Neq.__name__: NeqSchema,
        # --- String Conditions ---
        Contains.__name__: ContainsSchema,
        NotContains.__name__: NotContainsSchema,
        Equals.__name__: EqualsSchema,
        NotEquals.__name__: NotEqualsSchema,
        StartsWith.__name__: StartsWithSchema,
        EndsWith.__name__: EndsWithSchema,
        RegexMatch.__name__: RegexMatchSchema,
        # --- Collection Conditions ---
        IsIn.__name__: IsInSchema,
        IsNotIn.__name__: IsNotInSchema,
        AllIn.__name__: AllInSchema,
        AllNotIn.__name__: AllNotInSchema,
        AnyIn.__name__: AnyInSchema,
        AnyNotIn.__name__: AnyNotInSchema,
        IsEmpty.__name__: IsEmptySchema,
        IsNotEmpty.__name__: IsNotEmptySchema,
        # --- Logic Conditions ---
        And.__name__: AndSchema,
        Or.__name__: OrSchema,
        Not.__name__: NotSchema,
        # --- Other Conditions ---
        CIDR.__name__: CIDRSchema,
        Exists.__name__: ExistsSchema,
        NotExists.__name__: NotExistsSchema,
        Any.__name__: AnySchema,
    }
