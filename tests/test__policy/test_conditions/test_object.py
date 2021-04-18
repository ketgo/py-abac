"""
    Object condition tests
"""

import pytest
from marshmallow import ValidationError

from py_abac.context import EvaluationContext
from py_abac.policy.conditions.object import EqualsObject
from py_abac.policy.conditions.schema import ConditionSchema
from py_abac.request import AccessRequest


class TestCollectionCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (EqualsObject({}), {"condition": "EqualsObject", "value": {}}),
        (EqualsObject({"test": 2}), {"condition": "EqualsObject", "value": {"test": 2}}),
    ])
    def test_to_json(self, condition, condition_json):
        assert ConditionSchema().dump(condition) == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (EqualsObject({}), {"condition": "EqualsObject", "value": {}}),
        (EqualsObject({"test": 2}), {"condition": "EqualsObject", "value": {"test": 2}}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = ConditionSchema().load(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("data", [
        {"condition": "EqualsObject", "value": None},
        {"condition": "EqualsObject", "value": 2},
    ])
    def test_create_error(self, data):
        with pytest.raises(ValidationError):
            ConditionSchema().load(data)

    @pytest.mark.parametrize("condition, what, result", [
        (EqualsObject({}), {}, True),
        (EqualsObject({'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []}),
         {'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []}, True),
        (EqualsObject({'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []}), {'a': {'b': [1], 'd': 'test'}, 'e': []},
         False),
        (EqualsObject({'a': {'b': [1, {'c': 1}], 'd': 'test'}, 'e': []}), {'a': {'b': [1, {'c': 1}], 'd': 'test'}},
         False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
