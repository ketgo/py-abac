"""
    Policy rules tests
"""

import pytest
from marshmallow import ValidationError

from py_abac.context import EvaluationContext
from py_abac.policy.conditions.numeric import Eq
from py_abac.policy.conditions.string import Equals
from py_abac.policy.rules import Rules, RulesSchema
from py_abac.request import AccessRequest


def test_create():
    rules_json = {
        "subject": {"$.uid": {"condition": "Eq", "value": 1.0}},
        "resource": [{"$.name": {"condition": "Equals", "value": "test"}}],
        "action": {},
        "context": {}
    }
    rules = RulesSchema().load(rules_json)
    assert isinstance(rules, Rules)
    assert isinstance(rules.subject["$.uid"], Eq)
    assert rules.subject["$.uid"].value == 1.0
    assert isinstance(rules.resource[0]["$.name"], Equals)
    assert rules.resource[0]["$.name"].value == "test"
    assert rules.action == {}
    assert rules.context == {}

    rules_json = {
        "subject": {"$.uid": {"condition": "Eq", "value": 1.0}},
    }
    rules = RulesSchema().load(rules_json)
    assert isinstance(rules, Rules)
    assert isinstance(rules.subject["$.uid"], Eq)
    assert rules.subject["$.uid"].value == 1.0
    assert rules.resource == {}
    assert rules.action == {}
    assert rules.context == {}


@pytest.mark.parametrize("rules_json", [
    {"subject": None},
    {"subject": {}, "resource": None},
    {"subject": {}, "resource": {}, "action": None},
    {"subject": {}, "resource": {}, "action": {}, "context": None},
    {"subject": {"condition": "Eq", "value": 1.0}},
    {"subject": {}, "resource": {"condition": "Eq", "value": 1.0}},
    {"subject": {}, "resource": {}, "action": {"condition": "Eq", "value": 1.0}},
    {"subject": {}, "resource": {}, "action": {}, "context": {"condition": "Eq", "value": 1.0}},
    {"subject": [{"condition": "Eq", "value": 1.0}]},
    {"subject": {}, "resource": [{"condition": "Eq", "value": 1.0}]},
    {"subject": {}, "resource": {}, "action": [{"condition": "Eq", "value": 1.0}]},
    {"subject": {}, "resource": {}, "action": {}, "context": [{"condition": "Eq", "value": 1.0}]},
])
def test_create_error(rules_json):
    with pytest.raises(ValidationError):
        RulesSchema().load(rules_json)


@pytest.mark.parametrize("rules_json, result", [
    ({
         "subject": {"$.uid": {"condition": "Eq", "value": 1.0}},
         "resource": [{"$.name": {"condition": "Equals", "value": "test"}}],
         "action": {},
         "context": {}
     }, False),
    ({
         "subject": {"$.firstName": {"condition": "Equals", "value": "Carl"},
                     "$.lastName": {"condition": "Equals", "value": "Right"}},
         "resource": [{"$.name": {"condition": "Equals", "value": "test"}}],
         "action": {},
         "context": {}
     }, False),
    ({
         "subject": {"$.firstName": {"condition": "Equals", "value": "Carl"},
                     "$.lastName": {"condition": "Equals", "value": "Right"}},
         "resource": [{"$.name": {"condition": "Equals", "value": "test"}},
                      {"$.name": {"condition": "Equals", "value": "Calendar"}}],
         "action": {},
         "context": {}
     }, True),
    ({
         "subject": {"$.firstName": {"condition": "Equals", "value": "Carl"},
                     "$.lastName": {"condition": "Equals", "value": "Right"}},
         "resource": [{"$.name": {"condition": "Equals", "value": "Calendar"}}],
         "action": {},
         "context": {}
     }, True),
    ({
         "subject": {"$.firstName": {"condition": "Equals", "value": "Carl"},
                     "$.lastName": {"condition": "Equals", "value": "Right"}},
         "resource": [{"$.name": {"condition": "Equals", "value": "Calendar"}}],
         "action": {"$.method": {"condition": "Equals", "value": "Get"}},
         "context": {}
     }, False),
    ({
         "subject": {"$.firstName": {"condition": "Equals", "value": "Carl"},
                     "$.lastName": {"condition": "Equals", "value": "Right"},
                     "$.middleName": {"condition": "Equals", "value": "Marvin"}},
         "resource": [{"$.name": {"condition": "Equals", "value": "Calendar"}}],
         "action": {"$.method": {"condition": "Equals", "value": "Get"}},
         "context": {}
     }, False),
    ({
         "subject": {},
         "resource": {},
         "action": {},
         "context": {}
     }, True),
    ({
         "subject": [],
         "resource": [],
         "action": [],
         "context": []
     }, False),
])
def test_is_satisfied(rules_json, result):
    request_json = {
        "subject": {
            "id": "a",
            "attributes": {
                "firstName": "Carl",
                "lastName": "Right"
            }
        },
        "resource": {
            "id": "a",
            "attributes": {
                "name": "Calendar"
            }
        },
        "action": {
            "id": "",
            "attributes": {}
        },
        "context": {}
    }
    request = AccessRequest.from_json(request_json)
    ctx = EvaluationContext(request)
    rules = RulesSchema().load(rules_json)
    assert rules.is_satisfied(ctx) == result
