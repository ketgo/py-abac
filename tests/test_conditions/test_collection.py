"""
    Collection condition tests
"""

import pytest
from marshmallow import ValidationError

from py_abac.condition.collection import AllIn
from py_abac.condition.collection import AllNotIn
from py_abac.condition.collection import AnyIn
from py_abac.condition.collection import AnyNotIn
from py_abac.condition.collection import IsEmpty
from py_abac.condition.collection import IsIn
from py_abac.condition.collection import IsNotEmpty
from py_abac.condition.collection import IsNotIn
from py_abac.condition.schema import ConditionSchema
from py_abac.context import EvaluationContext
from py_abac.request import Request


class TestCollectionCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (AllIn([2]), {"condition": "AllIn", "value": [2]}),
        (AllNotIn([{"test": 2}]), {"condition": "AllNotIn", "value": [{"test": 2}]}),
        (AnyIn([2, {"test": 2}]), {"condition": "AnyIn", "value": [2, {"test": 2}]}),
        (AnyNotIn([2, {"test": 2}, []]), {"condition": "AnyNotIn", "value": [2, {"test": 2}, []]}),
        (IsIn([2]), {"condition": "IsIn", "value": [2]}),
        (IsNotIn([2]), {"condition": "IsNotIn", "value": [2]}),
        (IsEmpty(), {"condition": "IsEmpty"}),
        (IsNotEmpty(), {"condition": "IsNotEmpty"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert ConditionSchema().dump(condition) == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (AllIn([2]), {"condition": "AllIn", "value": [2]}),
        (AllNotIn([{"test": 2}]), {"condition": "AllNotIn", "value": [{"test": 2}]}),
        (AnyIn([2, {"test": 2}]), {"condition": "AnyIn", "value": [2, {"test": 2}]}),
        (AnyNotIn([2, {"test": 2}, []]), {"condition": "AnyNotIn", "value": [2, {"test": 2}, []]}),
        (IsIn([2]), {"condition": "IsIn", "value": [2]}),
        (IsNotIn([2]), {"condition": "IsNotIn", "value": [2]}),
        (IsEmpty(), {"condition": "IsEmpty"}),
        (IsNotEmpty(), {"condition": "IsNotEmpty"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = ConditionSchema().load(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition_type, data", [
        (AllIn, {"condition": "AllIn", "value": "test"}),
        (AllNotIn, {"condition": "AllNotIn", "value": 1}),
        (AnyIn, {"condition": "AnyIn", "value": {}}),
        (AnyNotIn, {"condition": "AnyNotIn", "value": None}),
        (IsIn, {"condition": "IsIn", "value": 1.0}),
        (IsNotIn, {"condition": "IsNotIn", "value": object}),
        (IsEmpty, {"condition": "IsEmpty", "value": []}),
        (IsNotEmpty, {"condition": "IsNotEmpty", "value": 1}),
    ])
    def test_create_error(self, condition_type, data):
        with pytest.raises(ValidationError):
            ConditionSchema().load(data)

    @pytest.mark.parametrize("condition, what, result", [
        (AllIn([]), 1, False),
        (AllIn([]), [], True),
        (AllIn([2]), [], True),
        (AllIn([2]), [2], True),
        (AllIn([2]), [1, 2], False),
        (AllIn([3, 2]), [1, 2], False),
        (AllIn([1, 2, 3]), [1, 2], True),
        (AllIn([1, 2, 3]), None, False),

        (AllNotIn([]), 1, False),
        (AllNotIn([]), [], False),
        (AllNotIn([2]), [], False),
        (AllNotIn([2]), [2], False),
        (AllNotIn([2]), [1, 2], True),
        (AllNotIn([3, 2]), [1, 2], True),
        (AllNotIn([1, 2, 3]), [1, 2], False),
        (AllNotIn([1, 2, 3]), None, False),

        (AnyIn([]), 1, False),
        (AnyIn([]), [], False),
        (AnyIn([2]), [], False),
        (AnyIn([2]), [2], True),
        (AnyIn([2]), [1, 2], True),
        (AnyIn([3, 2]), [1, 4], False),
        (AnyIn([1, 2, 3]), [1, 2], True),
        (AnyIn([1, 2, 3]), None, False),

        (AnyNotIn([]), 1, False),
        (AnyNotIn([]), [], True),
        (AnyNotIn([2]), [], True),
        (AnyNotIn([2]), [2], False),
        (AnyNotIn([2]), [1, 2], False),
        (AnyNotIn([3, 2]), [1, 4], True),
        (AnyNotIn([1, 2, 3]), [1, 2], False),
        (AnyNotIn([1, 2, 3]), None, False),

        (IsIn([]), [], False),
        (IsIn([1, 2, 3]), 1, True),
        (IsIn([1, 2, 3]), 4, False),
        (IsIn([1, 2, 3]), None, False),

        (IsNotIn([]), [], True),
        (IsNotIn([1, 2, 3]), 1, False),
        (IsNotIn([1, 2, 3]), 4, True),
        (IsNotIn([1, 2, 3]), None, True),

        (IsEmpty(), [], True),
        (IsEmpty(), [1], False),
        (IsEmpty(), None, False),

        (IsNotEmpty(), [], False),
        (IsNotEmpty(), [1], True),
        (IsNotEmpty(), None, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = Request(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
