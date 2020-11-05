"""
    Attribute conditions tests
"""

import pytest
from marshmallow import ValidationError

from py_abac.context import EvaluationContext
from py_abac.policy.conditions.attribute import AllInAttribute
from py_abac.policy.conditions.attribute import AllNotInAttribute
from py_abac.policy.conditions.attribute import AnyInAttribute
from py_abac.policy.conditions.attribute import AnyNotInAttribute
from py_abac.policy.conditions.attribute import EqualsAttribute
from py_abac.policy.conditions.attribute import IsInAttribute
from py_abac.policy.conditions.attribute import IsNotInAttribute
from py_abac.policy.conditions.attribute import NotEqualsAttribute
from py_abac.policy.conditions.schema import ConditionSchema
from py_abac.request import AccessRequest


class TestAttributeCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (
                EqualsAttribute("subject", "$.name"),
                {"condition": "EqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                NotEqualsAttribute("subject", "$.name"),
                {"condition": "NotEqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                IsInAttribute("subject", "$.teams"),
                {"condition": "IsInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                IsNotInAttribute("subject", "$.teams"),
                {"condition": "IsNotInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                AllInAttribute("subject", "$.name"),
                {"condition": "AllInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AllNotInAttribute("subject", "$.name"),
                {"condition": "AllNotInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyInAttribute("subject", "$.name"),
                {"condition": "AnyInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyNotInAttribute("subject", "$.name"),
                {"condition": "AnyNotInAttribute", "ace": "subject", "path": "$.name"}
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
                NotEqualsAttribute("subject", "$.name"),
                {"condition": "NotEqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                IsInAttribute("subject", "$.teams"),
                {"condition": "IsInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                IsNotInAttribute("subject", "$.teams"),
                {"condition": "IsNotInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                AllInAttribute("subject", "$.name"),
                {"condition": "AllInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AllNotInAttribute("subject", "$.name"),
                {"condition": "AllNotInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyInAttribute("subject", "$.name"),
                {"condition": "AnyInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyNotInAttribute("subject", "$.name"),
                {"condition": "AnyNotInAttribute", "ace": "subject", "path": "$.name"}
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

        {"condition": "NotEqualsAttribute", "ace": "test", "path": "$.name"},
        {"condition": "NotEqualsAttribute", "ace": "subject", "path": ")"},
        {"condition": "NotEqualsAttribute", "ace": "subject", "path": None},

        {"condition": "IsInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "IsInAttribute", "ace": "subject", "path": ")"},
        {"condition": "IsInAttribute", "ace": "subject", "path": None},

        {"condition": "IsNotInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "IsNotInAttribute", "ace": "subject", "path": ")"},
        {"condition": "IsNotInAttribute", "ace": "subject", "path": None},

        {"condition": "AllInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "AllInAttribute", "ace": "subject", "path": ")"},
        {"condition": "AllInAttribute", "ace": "subject", "path": None},

        {"condition": "AllNotInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "AllNotInAttribute", "ace": "subject", "path": ")"},
        {"condition": "AllNotInAttribute", "ace": "subject", "path": None},

        {"condition": "AnyInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "AnyInAttribute", "ace": "subject", "path": ")"},
        {"condition": "AnyInAttribute", "ace": "subject", "path": None},

        {"condition": "AnyNotInAttribute", "ace": "test", "path": "$.name"},
        {"condition": "AnyNotInAttribute", "ace": "subject", "path": ")"},
        {"condition": "AnyNotInAttribute", "ace": "subject", "path": None},
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
        (NotEqualsAttribute("subject", "$.what"), "test", False),
        (NotEqualsAttribute("resource", "$.what"), "test", True),
        (NotEqualsAttribute("resource", "$.*"), "test", True),
        (NotEqualsAttribute("resource", "$.name"), "test", True),
        (NotEqualsAttribute("resource", "$.name.what"), {"test": True}, False),
    ])
    def test_is_satisfied_not_equals_attribute(self, condition, what, result):
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

    @pytest.mark.parametrize("condition, what, result", [
        (AllInAttribute("subject", "$.what"), "test", False),
        (AllInAttribute("subject", "$.what"), ["test"], True),
        (AllInAttribute("resource", "$.what"), ["test"], False),
        (AllInAttribute("resource", "$.*"), ["test"], False),
        (AllInAttribute("resource", "$.name"), ["test"], False),
        (AllInAttribute("resource", "$.name.what"), ["test_1"], True),
        (AllInAttribute("resource", "$.name.what"), ["test_1", "test_2"], False),
    ])
    def test_is_satisfied_all_in_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": ["test_1"]}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result

    @pytest.mark.parametrize("condition, what, result", [
        (AllNotInAttribute("subject", "$.what"), "test", False),
        (AllNotInAttribute("subject", "$.what"), ["test"], False),
        (AllNotInAttribute("resource", "$.what"), ["test"], False),
        (AllNotInAttribute("resource", "$.*"), ["test"], False),
        (AllNotInAttribute("resource", "$.name"), ["test"], False),
        (AllNotInAttribute("resource", "$.name.what"), ["test_1"], False),
        (AllNotInAttribute("resource", "$.name.what"), ["test_1", "test_2"], True),
    ])
    def test_is_satisfied_all_not_in_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": ["test_1"]}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result

    @pytest.mark.parametrize("condition, what, result", [
        (AnyInAttribute("subject", "$.what"), "test", False),
        (AnyInAttribute("subject", "$.what"), ["test"], True),
        (AnyInAttribute("resource", "$.what"), ["test"], False),
        (AnyInAttribute("resource", "$.*"), ["test"], False),
        (AnyInAttribute("resource", "$.name"), ["test"], False),
        (AnyInAttribute("resource", "$.name.what"), ["test_1"], True),
        (AnyInAttribute("resource", "$.name.what"), ["test_1", "test_2"], True),
    ])
    def test_is_satisfied_any_in_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": ["test_1"]}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result

    @pytest.mark.parametrize("condition, what, result", [
        (AnyNotInAttribute("subject", "$.what"), "test", False),
        (AnyNotInAttribute("subject", "$.what"), ["test"], False),
        (AnyNotInAttribute("resource", "$.what"), ["test"], False),
        (AnyNotInAttribute("resource", "$.*"), ["test"], False),
        (AnyNotInAttribute("resource", "$.name"), ["test"], False),
        (AnyNotInAttribute("resource", "$.name.what"), ["test_3"], True),
        (AnyNotInAttribute("resource", "$.name.what"), ["test_1", "test_2"], False),
    ])
    def test_is_satisfied_any_not_in_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": ["test_1"]}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
