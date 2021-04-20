"""
    Attribute conditions tests
"""

import pytest
from pydantic import ValidationError

from py_abac._policy.conditions.attribute import AllInAttribute
from py_abac._policy.conditions.attribute import AllNotInAttribute
from py_abac._policy.conditions.attribute import AnyInAttribute
from py_abac._policy.conditions.attribute import AnyNotInAttribute
from py_abac._policy.conditions.attribute import EqualsAttribute
from py_abac._policy.conditions.attribute import IsInAttribute
from py_abac._policy.conditions.attribute import IsNotInAttribute
from py_abac._policy.conditions.attribute import NotEqualsAttribute
from py_abac.context import EvaluationContext
from py_abac.request import AccessRequest


class TestAttributeCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (
                EqualsAttribute(ace="subject", path="$.name"),
                {"condition": "EqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                NotEqualsAttribute(ace="subject", path="$.name"),
                {"condition": "NotEqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                IsInAttribute(ace="subject", path="$.teams"),
                {"condition": "IsInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                IsNotInAttribute(ace="subject", path="$.teams"),
                {"condition": "IsNotInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                AllInAttribute(ace="subject", path="$.name"),
                {"condition": "AllInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AllNotInAttribute(ace="subject", path="$.name"),
                {"condition": "AllNotInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyInAttribute(ace="subject", path="$.name"),
                {"condition": "AnyInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyNotInAttribute(ace="subject", path="$.name"),
                {"condition": "AnyNotInAttribute", "ace": "subject", "path": "$.name"}
        ),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.dict() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (
                EqualsAttribute(ace="subject", path="$.name"),
                {"condition": "EqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                NotEqualsAttribute(ace="subject", path="$.name"),
                {"condition": "NotEqualsAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                IsInAttribute(ace="subject", path="$.teams"),
                {"condition": "IsInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                IsNotInAttribute(ace="subject", path="$.teams"),
                {"condition": "IsNotInAttribute", "ace": "subject", "path": "$.teams"}
        ),
        (
                AllInAttribute(ace="subject", path="$.name"),
                {"condition": "AllInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AllNotInAttribute(ace="subject", path="$.name"),
                {"condition": "AllNotInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyInAttribute(ace="subject", path="$.name"),
                {"condition": "AnyInAttribute", "ace": "subject", "path": "$.name"}
        ),
        (
                AnyNotInAttribute(ace="subject", path="$.name"),
                {"condition": "AnyNotInAttribute", "ace": "subject", "path": "$.name"}
        ),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.parse_obj(condition_json)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition_type, data", [
        (EqualsAttribute, {"condition": "EqualsAttribute", "ace": "test", "path": "$.name"}),
        (EqualsAttribute, {"condition": "EqualsAttribute", "ace": "subject", "path": ")"}),
        (EqualsAttribute, {"condition": "EqualsAttribute", "ace": "subject", "path": None}),

        (NotEqualsAttribute, {"condition": "NotEqualsAttribute", "ace": "test", "path": "$.name"}),
        (NotEqualsAttribute, {"condition": "NotEqualsAttribute", "ace": "subject", "path": ")"}),
        (NotEqualsAttribute, {"condition": "NotEqualsAttribute", "ace": "subject", "path": None}),

        (IsInAttribute, {"condition": "IsInAttribute", "ace": "test", "path": "$.name"}),
        (IsInAttribute, {"condition": "IsInAttribute", "ace": "subject", "path": ")"}),
        (IsInAttribute, {"condition": "IsInAttribute", "ace": "subject", "path": None}),

        (IsNotInAttribute, {"condition": "IsNotInAttribute", "ace": "test", "path": "$.name"}),
        (IsNotInAttribute, {"condition": "IsNotInAttribute", "ace": "subject", "path": ")"}),
        (IsNotInAttribute, {"condition": "IsNotInAttribute", "ace": "subject", "path": None}),

        (AllInAttribute, {"condition": "AllInAttribute", "ace": "test", "path": "$.name"}),
        (AllInAttribute, {"condition": "AllInAttribute", "ace": "subject", "path": ")"}),
        (AllInAttribute, {"condition": "AllInAttribute", "ace": "subject", "path": None}),

        (AllNotInAttribute, {"condition": "AllNotInAttribute", "ace": "test", "path": "$.name"}),
        (AllNotInAttribute, {"condition": "AllNotInAttribute", "ace": "subject", "path": ")"}),
        (AllNotInAttribute, {"condition": "AllNotInAttribute", "ace": "subject", "path": None}),

        (AnyInAttribute, {"condition": "AnyInAttribute", "ace": "test", "path": "$.name"}),
        (AnyInAttribute, {"condition": "AnyInAttribute", "ace": "subject", "path": ")"}),
        (AnyInAttribute, {"condition": "AnyInAttribute", "ace": "subject", "path": None}),

        (AnyNotInAttribute, {"condition": "AnyNotInAttribute", "ace": "test", "path": "$.name"}),
        (AnyNotInAttribute, {"condition": "AnyNotInAttribute", "ace": "subject", "path": ")"}),
        (AnyNotInAttribute, {"condition": "AnyNotInAttribute", "ace": "subject", "path": None}),
    ])
    def test_create_error(self, condition_type, data):
        with pytest.raises(ValidationError):
            condition_type.parse_obj(data)

    @pytest.mark.parametrize("condition, what, result", [
        (EqualsAttribute(ace="subject", path="$.what"), "test", True),
        (EqualsAttribute(ace="resource", path="$.what"), "test", False),
        (EqualsAttribute(ace="resource", path="$.*"), "test", False),
        (EqualsAttribute(ace="resource", path="$.name"), "test", False),
        (EqualsAttribute(ace="resource", path="$.name.what"), {"test": True}, True),
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
        (NotEqualsAttribute(ace="subject", path="$.what"), "test", False),
        (NotEqualsAttribute(ace="resource", path="$.what"), "test", True),
        (NotEqualsAttribute(ace="resource", path="$.*"), "test", True),
        (NotEqualsAttribute(ace="resource", path="$.name"), "test", True),
        (NotEqualsAttribute(ace="resource", path="$.name.what"), {"test": True}, False),
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
        (IsInAttribute(ace="subject", path="$.what"), "test", False),
        (IsInAttribute(ace="resource", path="$.what"), "test", False),
        (IsInAttribute(ace="resource", path="$.*"), "test", False),
        (IsInAttribute(ace="resource", path="$.name"), "test", False),
        (IsInAttribute(ace="resource", path="$.name.what"), "test", True),
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
        (IsNotInAttribute(ace="subject", path="$.what"), "test", False),
        (IsNotInAttribute(ace="resource", path="$.what"), "test", False),
        (IsNotInAttribute(ace="resource", path="$.*"), "test", False),
        (IsNotInAttribute(ace="resource", path="$.name"), "test", False),
        (IsNotInAttribute(ace="resource", path="$.name.what"), "test", True),
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
        (AllInAttribute(ace="subject", path="$.what"), "test", False),
        (AllInAttribute(ace="subject", path="$.what"), ["test"], True),
        (AllInAttribute(ace="resource", path="$.what"), ["test"], False),
        (AllInAttribute(ace="resource", path="$.*"), ["test"], False),
        (AllInAttribute(ace="resource", path="$.name"), ["test"], False),
        (AllInAttribute(ace="resource", path="$.name.what"), ["test_1"], True),
        (AllInAttribute(ace="resource", path="$.name.what"), ["test_1", "test_2"], False),
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
        (AllNotInAttribute(ace="subject", path="$.what"), "test", False),
        (AllNotInAttribute(ace="subject", path="$.what"), ["test"], False),
        (AllNotInAttribute(ace="resource", path="$.what"), ["test"], False),
        (AllNotInAttribute(ace="resource", path="$.*"), ["test"], False),
        (AllNotInAttribute(ace="resource", path="$.name"), ["test"], False),
        (AllNotInAttribute(ace="resource", path="$.name.what"), ["test_1"], False),
        (AllNotInAttribute(ace="resource", path="$.name.what"), ["test_1", "test_2"], True),
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
        (AnyInAttribute(ace="subject", path="$.what"), "test", False),
        (AnyInAttribute(ace="subject", path="$.what"), ["test"], True),
        (AnyInAttribute(ace="resource", path="$.what"), ["test"], False),
        (AnyInAttribute(ace="resource", path="$.*"), ["test"], False),
        (AnyInAttribute(ace="resource", path="$.name"), ["test"], False),
        (AnyInAttribute(ace="resource", path="$.name.what"), ["test_1"], True),
        (AnyInAttribute(ace="resource", path="$.name.what"), ["test_1", "test_2"], True),
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
        (AnyNotInAttribute(ace="subject", path="$.what"), "test", False),
        (AnyNotInAttribute(ace="subject", path="$.what"), ["test"], False),
        (AnyNotInAttribute(ace="resource", path="$.what"), ["test"], False),
        (AnyNotInAttribute(ace="resource", path="$.*"), ["test"], False),
        (AnyNotInAttribute(ace="resource", path="$.name"), ["test"], False),
        (AnyNotInAttribute(ace="resource", path="$.name.what"), ["test_3"], True),
        (AnyNotInAttribute(ace="resource", path="$.name.what"), ["test_1", "test_2"], False),
    ])
    def test_is_satisfied_any_not_in_attribute(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": ["test_1"]}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
