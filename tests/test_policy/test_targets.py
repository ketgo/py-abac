"""
    Policy target tests
"""

import pytest
from marshmallow import ValidationError

from py_abac.policy.context import EvaluationContext
from py_abac.policy.targets import Targets, TargetsSchema
from py_abac.request import Request


def test_create():
    targets_json = {
        "subject_id": ["abc", "a*"],
        "resource_id": ["123"],
    }
    targets = TargetsSchema().load(targets_json)
    assert isinstance(targets, Targets)
    assert targets.subject_id == targets_json["subject_id"]
    assert targets.resource_id == targets_json["resource_id"]
    assert targets.action_id == "*"


@pytest.mark.parametrize("targets_json", [
    {"subject_id": [None, ]},
    {"resource_id": [{}, ]},
    {"action_id": {}},
    {"subject_id": [""]},
    {"resource_id": ""},
])
def test_create_error(targets_json):
    with pytest.raises(ValidationError):
        TargetsSchema().load(targets_json)


@pytest.mark.parametrize("targets_json, result", [
    ({}, True),
    ({"subject_id": "abc"}, True),
    ({"subject_id": "ab*"}, True),
    ({"subject_id": "abd"}, False),
    ({"subject_id": ["abd", "ab*"]}, True),
    ({"subject_id": "ab*", "resource_id": "1*"}, True),
    ({"subject_id": "ab*", "resource_id": "1*", "action_id": "1"}, False),
])
def test_match(targets_json, result):
    request_json = {
        "subject": {
            "id": "abc",
            "attributes": {
                "firstName": "Carl",
                "lastName": "Right"
            }
        },
        "resource": {
            "id": "12",
            "attributes": {
                "name": "Calendar"
            }
        },
        "action": {
            "id": ">",
            "attributes": {}
        },
        "context": {}
    }
    request = Request.from_json(request_json)
    ctx = EvaluationContext(request)
    targets = TargetsSchema().load(targets_json)
    assert targets.match(ctx) == result
