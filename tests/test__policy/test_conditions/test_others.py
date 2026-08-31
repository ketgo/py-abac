"""
    Other condition tests
"""

import pytest
from pydantic import ValidationError

from py_abac._policy.conditions.others import Any
from py_abac._policy.conditions.others import CIDR
from py_abac._policy.conditions.others import Exists
from py_abac._policy.conditions.others import NotExists
from py_abac.context import EvaluationContext
from py_abac.request import AccessRequest


class TestOtherCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDR(value="127.0.0.0/16"), {"condition": "CIDR", "value": "127.0.0.0/16"}),
        (Exists(), {"condition": "Exists"}),
        (NotExists(), {"condition": "NotExists"}),
        (Any(), {"condition": "Any"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.dict() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDR(value="127.0.0.0/16"), {"condition": "CIDR", "value": "127.0.0.0/16"}),
        (Exists(), {"condition": "Exists"}),
        (NotExists(), {"condition": "NotExists"}),
        (Any(), {"condition": "Any"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.parse_obj(condition_json)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("data", [
        {"condition": "CIDR", "value": 1.0},
    ])
    def test_create_error(self, data):
        with pytest.raises(ValidationError):
            CIDR.parse_obj(data)

    @pytest.mark.parametrize("condition, what, result", [
        (CIDR(value="127.0.0.0/24"), "10.0.0.0", False),
        (CIDR(value="127.0.0.0/24"), "127.0.0.1", True),
        (CIDR(value="127.0.0.0/24"), ")", False),
        (CIDR(value="127.0.0.0/24"), None, False),

        (Exists(), None, False),
        (Exists(), 1.0, True),

        (NotExists(), None, True),
        (NotExists(), 1.0, False),

        (Any(), None, True),
        (Any(), 1.0, True),
        (Any(), {"value": 1.0}, True),
        (Any(), [1.0, 2.0, "a"], True),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}},
                                resource={"attributes": {"name": {"what": what}}},
                                action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
