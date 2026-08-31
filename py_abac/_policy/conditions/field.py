"""
    Condition one-of schema
"""

from .attribute.all_in import AllInAttribute
from .attribute.all_not_in import AllNotInAttribute
from .attribute.any_in import AnyInAttribute
from .attribute.any_not_in import AnyNotInAttribute
# -- Attribute Conditions ---
from .attribute.equals import EqualsAttribute
from .attribute.is_in import IsInAttribute
from .attribute.is_not_in import IsNotInAttribute
from .attribute.not_equals import NotEqualsAttribute
# --- Collection Conditions ---
from .collection.all_in import AllIn
from .collection.all_not_in import AllNotIn
from .collection.any_in import AnyIn
from .collection.any_not_in import AnyNotIn
from .collection.is_empty import IsEmpty
from .collection.is_in import IsIn
from .collection.is_not_empty import IsNotEmpty
from .collection.is_not_in import IsNotIn
# --- Logic Conditions ---
from .logic.all_of import AllOf
from .logic.any_of import AnyOf
from .logic.not_ import Not
# --- Numeric Conditions ---
from .numeric.eq import Eq
from .numeric.gt import Gt
from .numeric.gte import Gte
from .numeric.lt import Lt
from .numeric.lte import Lte
from .numeric.neq import Neq
# --- Object Conditions ---
from .object.equals_object import EqualsObject
# --- Other Conditions ---
from .others.any import Any
from .others.cidr import CIDR
from .others.exists import Exists
from .others.not_exists import NotExists
# --- String Conditions ---
from .string.contains import Contains
from .string.ends_with import EndsWith
from .string.equals import Equals
from .string.not_contains import NotContains
from .string.not_equals import NotEquals
from .string.regex_match import RegexMatch
from .string.starts_with import StartsWith


class ConditionField:
    """
        Polymorphic JSON field for conditions
    """
    type_field = "condition"
    type_schemas = {
        # --- Numeric Conditions ---
        Eq.__name__: Eq,
        Gt.__name__: Gt,
        Lt.__name__: Lt,
        Gte.__name__: Gte,
        Lte.__name__: Lte,
        Neq.__name__: Neq,
        # --- String Conditions ---
        Contains.__name__: Contains,
        NotContains.__name__: NotContains,
        Equals.__name__: Equals,
        NotEquals.__name__: NotEquals,
        StartsWith.__name__: StartsWith,
        EndsWith.__name__: EndsWith,
        RegexMatch.__name__: RegexMatch,
        # --- Collection Conditions ---
        IsIn.__name__: IsIn,
        IsNotIn.__name__: IsNotIn,
        AllIn.__name__: AllIn,
        AllNotIn.__name__: AllNotIn,
        AnyIn.__name__: AnyIn,
        AnyNotIn.__name__: AnyNotIn,
        IsEmpty.__name__: IsEmpty,
        IsNotEmpty.__name__: IsNotEmpty,
        # --- Logic Conditions ---
        AllOf.__name__: AllOf,
        AnyOf.__name__: AnyOf,
        Not.__name__: Not,
        # --- Other Conditions ---
        CIDR.__name__: CIDR,
        Exists.__name__: Exists,
        NotExists.__name__: NotExists,
        Any.__name__: Any,
        # --- Attribute Conditions ---
        EqualsAttribute.__name__: EqualsAttribute,
        NotEqualsAttribute.__name__: NotEqualsAttribute,
        AnyInAttribute.__name__: AnyInAttribute,
        AnyNotInAttribute.__name__: AnyNotInAttribute,
        AllInAttribute.__name__: AllInAttribute,
        AllNotInAttribute.__name__: AllNotInAttribute,
        IsInAttribute.__name__: IsInAttribute,
        IsNotInAttribute.__name__: IsNotInAttribute,
        # --- Object Condition ---
        EqualsObject.__name__: EqualsObject,
    }

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values):
        item_type = values[cls.type_field]
        condition = cls.type_schemas[item_type]
        return condition(**v)
