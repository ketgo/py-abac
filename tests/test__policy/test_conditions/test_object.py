"""
    Object condition tests
"""

import pytest
from pydantic import ValidationError

from py_abac._policy.conditions.object import EqualsObject
from py_abac.context import EvaluationContext
from py_abac.request import AccessRequest


class TestCollectionCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (EqualsObject(value={}), {"condition": "EqualsObject", "value": {}}),
        (EqualsObject(value={"test": 2}), {"condition": "EqualsObject", "value": {"test": 2}}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.dict() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (EqualsObject(value={}), {"condition": "EqualsObject", "value": {}}),
        (EqualsObject(value={"test": 2}), {"condition": "EqualsObject", "value": {"test": 2}}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.parse_obj(condition_json)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("data", [
        {"condition": "EqualsObject", "value": None},
        {"condition": "EqualsObject", "value": 2},
    ])
    def test_create_error(self, data):
        with pytest.raises(ValidationError):
            EqualsObject.parse_obj(data)

    @pytest.mark.parametrize("condition, what, result", [
        (EqualsObject(value={}),
         {},
         True),
        (EqualsObject(value={'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []}),
         {'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []},
         True),
        (EqualsObject(value={'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []}),
         {'a': {'b': [1], 'd': 'test'}, 'e': []},
         False),
        (EqualsObject(value={'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []}),
         {'a': {'b': [1, {'c': 1}], 'd': 'test'}},
         False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
