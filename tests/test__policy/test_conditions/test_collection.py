"""
    Collection condition tests
"""

import pytest
from pydantic import ValidationError

from py_abac._policy.conditions.collection import AllIn
from py_abac._policy.conditions.collection import AllNotIn
from py_abac._policy.conditions.collection import AnyIn
from py_abac._policy.conditions.collection import AnyNotIn
from py_abac._policy.conditions.collection import IsEmpty
from py_abac._policy.conditions.collection import IsIn
from py_abac._policy.conditions.collection import IsNotEmpty
from py_abac._policy.conditions.collection import IsNotIn
from py_abac.context import EvaluationContext
from py_abac.request import AccessRequest


class TestCollectionCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (AllIn(values=[2]), {"condition": "AllIn", "values": [2]}),
        (AllNotIn(values=[{"test": 2}]), {"condition": "AllNotIn", "values": [{"test": 2}]}),
        (AnyIn(values=[2, {"test": 2}]), {"condition": "AnyIn", "values": [2, {"test": 2}]}),
        (AnyNotIn(values=[2, {"test": 2}, []]), {"condition": "AnyNotIn", "values": [2, {"test": 2}, []]}),
        (IsIn(values=[2]), {"condition": "IsIn", "values": [2]}),
        (IsNotIn(values=[2]), {"condition": "IsNotIn", "values": [2]}),
        (IsEmpty(), {"condition": "IsEmpty"}),
        (IsNotEmpty(), {"condition": "IsNotEmpty"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.dict() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (AllIn(values=[2]), {"condition": "AllIn", "values": [2]}),
        (AllNotIn(values=[{"test": 2}]), {"condition": "AllNotIn", "values": [{"test": 2}]}),
        (AnyIn(values=[2, {"test": 2}]), {"condition": "AnyIn", "values": [2, {"test": 2}]}),
        (AnyNotIn(values=[2, {"test": 2}, []]), {"condition": "AnyNotIn", "values": [2, {"test": 2}, []]}),
        (IsIn(values=[2]), {"condition": "IsIn", "values": [2]}),
        (IsNotIn(values=[2]), {"condition": "IsNotIn", "values": [2]}),
        (IsEmpty(), {"condition": "IsEmpty"}),
        (IsNotEmpty(), {"condition": "IsNotEmpty"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.parse_obj(condition_json)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition_type, data", [
        (AllIn, {"condition": "AllIn", "values": "test"}),
        (AllNotIn, {"condition": "AllNotIn", "values": 1}),
        (AnyIn, {"condition": "AnyIn", "values": {}}),
        (AnyNotIn, {"condition": "AnyNotIn", "values": None}),
        (IsIn, {"condition": "IsIn", "values": 1.0}),
        (IsNotIn, {"condition": "IsNotIn", "values": object}),
        (IsEmpty, {"condition": "IsEmpty", "values": []}),
        (IsNotEmpty, {"condition": "IsNotEmpty", "values": 1}),
    ])
    def test_create_error(self, condition_type, data):
        with pytest.raises(ValidationError):
            condition_type.parse_obj(data)

    @pytest.mark.parametrize("condition, what, result", [
        (AllIn(values=[]), 1, False),
        (AllIn(values=[]), [], True),
        (AllIn(values=[2]), [], True),
        (AllIn(values=[2]), [2], True),
        (AllIn(values=[2]), [1, 2], False),
        (AllIn(values=[3, 2]), [1, 2], False),
        (AllIn(values=[1, 2, 3]), [1, 2], True),
        (AllIn(values=[1, 2, 3]), None, False),

        (AllNotIn(values=[]), 1, False),
        (AllNotIn(values=[]), [], False),
        (AllNotIn(values=[2]), [], False),
        (AllNotIn(values=[2]), [2], False),
        (AllNotIn(values=[2]), [1, 2], True),
        (AllNotIn(values=[3, 2]), [1, 2], True),
        (AllNotIn(values=[1, 2, 3]), [1, 2], False),
        (AllNotIn(values=[1, 2, 3]), None, False),

        (AnyIn(values=[]), 1, False),
        (AnyIn(values=[]), [], False),
        (AnyIn(values=[2]), [], False),
        (AnyIn(values=[2]), [2], True),
        (AnyIn(values=[2]), [1, 2], True),
        (AnyIn(values=[3, 2]), [1, 4], False),
        (AnyIn(values=[1, 2, 3]), [1, 2], True),
        (AnyIn(values=[1, 2, 3]), None, False),

        (AnyNotIn(values=[]), 1, False),
        (AnyNotIn(values=[]), [], True),
        (AnyNotIn(values=[2]), [], True),
        (AnyNotIn(values=[2]), [2], False),
        (AnyNotIn(values=[2]), [1, 2], False),
        (AnyNotIn(values=[3, 2]), [1, 4], True),
        (AnyNotIn(values=[1, 2, 3]), [1, 2], False),
        (AnyNotIn(values=[1, 2, 3]), None, False),

        (IsIn(values=[]), [], False),
        (IsIn(values=[1, 2, 3]), 1, True),
        (IsIn(values=[1, 2, 3]), 4, False),
        (IsIn(values=[1, 2, 3]), None, False),

        (IsNotIn(values=[]), [], True),
        (IsNotIn(values=[1, 2, 3]), 1, False),
        (IsNotIn(values=[1, 2, 3]), 4, True),
        (IsNotIn(values=[1, 2, 3]), None, True),

        (IsEmpty(), [], True),
        (IsEmpty(), [1], False),
        (IsEmpty(), None, False),

        (IsNotEmpty(), [], False),
        (IsNotEmpty(), [1], True),
        (IsNotEmpty(), None, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
