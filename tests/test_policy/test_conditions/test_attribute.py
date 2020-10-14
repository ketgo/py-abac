"""
    Attribute conditions tests
"""

import pytest
from marshmallow import ValidationError

from py_abac.context import EvaluationContext
from py_abac.policy.conditions.attribute import EqualsAttribute
from py_abac.policy.conditions.attribute import IsInAttribute
from py_abac.policy.conditions.attribute import IsNotInAttribute
from py_abac.policy.conditions.schema import ConditionSchema
from py_abac.request import AccessRequest


class TestAttributeCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (
                EqualsAttribute("subject", "$.name"),
                {"condition": "EqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                IsInAttribute("subject", "$.teams"),
                {"condition": "IsInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                IsNotInAttribute("subject", "$.teams"),
                {"condition": "IsNotInAttribute", "ace": "subject", "path": "$.teams"}
        ),
    ])
    def test_to_json(self, condition, condition_json):
        assert ConditionSchema().dump(condition) == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (
                EqualsAttribute("subject", "$.name"),
                {"condition": "EqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                IsInAttribute("subject", "$.teams"),
                {"condition": "IsInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                IsNotInAttribute("subject", "$.teams"),
                {"condition": "IsNotInAttribute", "ace": "subject", "path": "$.teams"}
        ),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = ConditionSchema().load(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("data", [
        {"condition": "EqualsAttribute", "ace": "test", "path": "$.name"},
        {"condition": "EqualsAttribute", "ace": "subject", "path": ")"},
        {"condition": "EqualsAttribute", "ace": "subject", "path": None},

        {"condition": "IsInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "IsInAttribute", "ace": "subject", "path": ")"},
        {"condition": "IsInAttribute", "ace": "subject", "path": None},

        {"condition": "IsNotInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "IsNotInAttribute", "ace": "subject", "path": ")"},
        {"condition": "IsNotInAttribute", "ace": "subject", "path": None},
    ])
    def test_create_error(self, data):
        with pytest.raises(ValidationError):
            ConditionSchema().load(data)

    @pytest.mark.parametrize("condition, what, result", [
        (EqualsAttribute("subject", "$.what"), "test", True),
        (EqualsAttribute("resource", "$.what"), "test", False),
        (EqualsAttribute("resource", "$.*"), "test", False),
        (EqualsAttribute("resource", "$.name"), "test", False),
        (EqualsAttribute("resource", "$.name.what"), {"test": True}, True),
    ])
    def test_is_satisfied_equals_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": what}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result

    @pytest.mark.parametrize("condition, what, result", [
        (IsInAttribute("subject", "$.what"), "test", False),
        (IsInAttribute("resource", "$.what"), "test", False),
        (IsInAttribute("resource", "$.*"), "test", False),
        (IsInAttribute("resource", "$.name"), "test", False),
        (IsInAttribute("resource", "$.name.what"), "test", True),
    ])
    def test_is_satisfied_is_in_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": ["test"]}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result

    @pytest.mark.parametrize("condition, what, result", [
        (IsNotInAttribute("subject", "$.what"), "test", False),
        (IsNotInAttribute("resource", "$.what"), "test", False),
        (IsNotInAttribute("resource", "$.*"), "test", False),
        (IsNotInAttribute("resource", "$.name"), "test", False),
        (IsNotInAttribute("resource", "$.name.what"), "test", True),
    ])
    def test_is_satisfied_is_not_in_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": ["test-2"]}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
