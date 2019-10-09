"""
    MongoDB policy model test
"""

import json

import pytest

from py_abac.policy import Policy
from py_abac.storage.mongo.model import PolicyModel, _split_id


def test_from_policy():
    policy_json = {
        "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
        "description": "Block user 'Max' when ip in CIDR 192.168.1.0/24",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "context": {"$.ip": {"condition": "Not",
                                 "value": {"condition": "CIDR", "value": "192.168.1.0/24"}}}
        },
        "targets": {
            "subject_id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb"
        },
        "effect": "deny"
    }
    policy = Policy.from_json(policy_json)
    model = PolicyModel.from_policy(policy)
    assert isinstance(model, PolicyModel)
    assert isinstance(model.policy_str, str)
    assert isinstance(model._id, str)
    assert isinstance(model.tags, dict)
    assert model.policy_str == json.dumps(policy.to_json())
    assert model._id == policy.uid
    assert model.tags == {"subject": [{"id": ["user::b90b2998-9e1b-4ac5-a743-b060b2634dbb"]}],
                          "resource": [{"id": ["*"]}],
                          "action": [{"id": ["*"]}]}


def test_to_policy():
    policy_json = {
        "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
        "description": "Block user 'Max' when ip in CIDR 192.168.1.0/24",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "context": {"$.ip": {"condition": "Not",
                                 "value": {"condition": "CIDR", "value": "192.168.1.0/24"}}}
        },
        "targets": {
            "subject_id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb"
        },
        "effect": "deny"
    }
    policy = Policy.from_json(policy_json)
    model = PolicyModel.from_policy(policy)
    new_policy = model.to_policy()
    assert policy.uid == new_policy.uid
    assert policy.description == new_policy.description
    assert policy.priority == new_policy.priority


def test_from_doc():
    policy_json = {
        "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
        "description": "Block user 'Max' when ip in CIDR 192.168.1.0/24",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "context": {"$.ip": {"condition": "Not",
                                 "value": {"condition": "CIDR", "value": "192.168.1.0/24"}}}
        },
        "targets": {
            "subject_id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb"
        },
        "effect": "deny"
    }
    policy = Policy.from_json(policy_json)
    policy_doc = {"_id": policy.uid, "policy_str": json.dumps(policy.to_json()), "tags": {}}
    model = PolicyModel.from_doc(policy_doc)
    assert model._id == policy_doc["_id"]
    assert model.policy_str == policy_doc["policy_str"]
    assert model.tags == policy_doc["tags"]


def test_to_doc():
    policy_json = {
        "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
        "description": "Block user 'Max' when ip in CIDR 192.168.1.0/24",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "context": {"$.ip": {"condition": "Not",
                                 "value": {"condition": "CIDR", "value": "192.168.1.0/24"}}}
        },
        "targets": {
            "subject_id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb"
        },
        "effect": "deny"
    }
    policy = Policy.from_json(policy_json)
    policy_doc = {"_id": policy.uid, "policy_str": json.dumps(policy.to_json()), "tags": {}}
    model = PolicyModel.from_doc(policy_doc)
    new_policy_doc = model.to_doc()
    assert policy_doc == new_policy_doc


@pytest.mark.parametrize("policy_json, tags", [
    (
            {
                "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
                "description": "Simple target match",
                "rules": {},
                "targets": {
                    "subject_id": "abc"
                },
                "effect": "deny"
            },
            {
                "subject": [
                    {"id": ["abc"]}
                ],
                "resource": [
                    {"id": ["*"]}
                ],
                "action": [
                    {"id": ["*"]}
                ]
            }
    ),
])
def test__targets_to_tags(policy_json, tags):
    policy = Policy.from_json(policy_json)
    assert PolicyModel._targets_to_tags(policy.targets) == tags


@pytest.mark.parametrize("string, splits", [
    ("a", ["a"]),
    ("*", ["*"]),

    ("ab", ["ab"]),
    ("a*", ["a*"]),
    ("*a", ["*a"]),
    ("**", ["*"]),

    ("abc", ["abc"]),
    ("*ab", ["*ab"]),
    ("a*b", ["a*", "*b"]),
    ("ab*", ["ab*"]),
    ("**a", ["*a"]),
    ("*a*", ["*a*"]),
    ("a**", ["a*"]),
    ("***", ["*"]),

    ("abcd", ["abcd"]),
    ("*abc", ["*abc"]),
    ("a*bc", ["a*", "*bc"]),
    ("ab*c", ["ab*", "*c"]),
    ("abc*", ["abc*"]),
    ("**ab", ["*ab"]),
    ("*a*b", ["*a*", "*b"]),
    ("*ab*", ["*ab*"]),
    ("a**b", ["a*", "*b"]),
    ("a*b*", ["a*", "*b*"]),
    ("ab**", ["ab*"]),
    ("***a", ["*a"]),
    ("a***", ["a*"]),
    ("****", ["*"]),
])
def test__split_id(string, splits):
    assert _split_id(string) == splits
