"""
    Numeric condition tests
"""

import pytest
from pydantic import ValidationError

from py_abac._policy.conditions.numeric import Eq
from py_abac._policy.conditions.numeric import Gt
from py_abac._policy.conditions.numeric import Gte
from py_abac._policy.conditions.numeric import Lt
from py_abac._policy.conditions.numeric import Lte
from py_abac._policy.conditions.numeric import Neq
from py_abac.context import EvaluationContext
from py_abac.request import AccessRequest


class TestNumericCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (Eq(value=2), {"condition": "Eq", "value": 2}),
        (Eq(value=3.0), {"condition": "Eq", "value": 3.0}),
        (Gt(value=2), {"condition": "Gt", "value": 2}),
        (Gt(value=3.0), {"condition": "Gt", "value": 3.0}),
        (Lt(value=2), {"condition": "Lt", "value": 2}),
        (Lt(value=3.0), {"condition": "Lt", "value": 3.0}),
        (Gte(value=2), {"condition": "Gte", "value": 2}),
        (Gte(value=3.0), {"condition": "Gte", "value": 3.0}),
        (Lte(value=2), {"condition": "Lte", "value": 2}),
        (Lte(value=3.0), {"condition": "Lte", "value": 3.0}),
        (Neq(value=2), {"condition": "Neq", "value": 2}),
        (Neq(value=3.0), {"condition": "Neq", "value": 3.0}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.dict() == condition_json

    @pytest.mark.parametrize("condition_type, value, condition_json", [
        (Eq, 2, {"condition": "Eq", "value": 2}),
        (Eq, 3.0, {"condition": "Eq", "value": 3.0}),
        (Gt, 2, {"condition": "Gt", "value": 2}),
        (Gt, 3.0, {"condition": "Gt", "value": 3.0}),
        (Lt, 2, {"condition": "Lt", "value": 2}),
        (Lt, 3.0, {"condition": "Lt", "value": 3.0}),
        (Gte, 2, {"condition": "Gte", "value": 2}),
        (Gte, 3.0, {"condition": "Gte", "value": 3.0}),
        (Lte, 2, {"condition": "Lte", "value": 2}),
        (Lte, 3.0, {"condition": "Lte", "value": 3.0}),
        (Neq, 2, {"condition": "Neq", "value": 2}),
        (Neq, 3.0, {"condition": "Neq", "value": 3.0}),
    ])
    def test_from_json(self, condition_type, value, condition_json):
        condition = condition_type.parse_obj(condition_json)
        assert condition.value == value

    @pytest.mark.parametrize("condition_type, data", [
        (Eq, {"condition": "Eq", "value": "test"}),
        (Gt, {"condition": "Gt", "value": []}),
        (Lt, {"condition": "Lt", "value": {}}),
        (Gte, {"condition": "Gte", "value": None}),
        (Lte, {"condition": "Lte", "value": {1, }}),
        (Neq, {"condition": "Neq", "value": ()}),
    ])
    def test_create_error(self, condition_type, data):
        with pytest.raises(ValidationError):
            condition_type.parse_obj(data)

    @pytest.mark.parametrize("condition, what, result", [
        (Eq(value=2), 2, True),
        (Eq(value=2), 2.0, True),
        (Eq(value=2.0), 2, True),
        (Eq(value=2.0), 2.0, True),
        (Eq(value=2), 3.0, False),
        (Eq(value=2), None, False),

        (Gt(value=2), 2, False),
        (Gt(value=2), 2.1, True),
        (Gt(value=2), 1.9, False),
        (Gt(value=2), None, False),

        (Gte(value=2), 2, True),
        (Gte(value=2), 2.1, True),
        (Gte(value=2), 1.9, False),
        (Gte(value=2), None, False),

        (Lt(value=2), 2, False),
        (Lt(value=2), 2.1, False),
        (Lt(value=2), 1.9, True),
        (Lt(value=2), None, False),

        (Lte(value=2), 2, True),
        (Lte(value=2), 2.1, False),
        (Lte(value=2), 1.9, True),
        (Lte(value=2), None, False),

        (Neq(value=2), 2, False),
        (Neq(value=2.0), 2, False),
        (Neq(value=2), 2.0, False),
        (Neq(value=2), 1.9, True),
        (Neq(value=2), None, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
