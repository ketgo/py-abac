"""
    Policy tests
"""

import uuid

import pytest

from py_abac.exceptions import PolicyCreateError
from py_abac.policy import Policy
from py_abac.policy.conditions.numeric import Eq
from py_abac.policy.conditions.string import Equals
from py_abac.policy.rules import Rules
from py_abac.policy.targets import Targets
from py_abac.request import Request


class TestPolicy(object):

    def test_create(self):
        uid = uuid.uuid4()
        policy_json = {
            "uid": str(uid),
            "description": "Policy create test",
            "rules": {
                "subject": {"$.uid": {"condition": "Eq", "value": 1.0}},
                "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
                "action": {},
                "context": {}
            },
            "targets": {
                "subject_id": ["abc", "a*"],
                "resource_id": ["123"],
                'action_id': '*'
            },
            "effect": "deny",
            "priority": 0
        }
        policy = Policy.from_json(policy_json)
        assert policy.to_json() == policy_json

        rules = policy.rules
        assert isinstance(rules, Rules)
        assert isinstance(rules.subject["$.uid"], Eq)
        assert rules.subject["$.uid"].value == 1.0
        assert isinstance(rules.resource[0]["$.name"], Equals)
        assert rules.resource[0]["$.name"].value == "test"
        assert rules.action == {}
        assert rules.context == {}

        targets = policy.targets
        targets_json = policy_json["targets"]
        assert isinstance(targets, Targets)
        assert targets.subject_id == targets_json["subject_id"]
        assert targets.resource_id == targets_json["resource_id"]
        assert targets.action_id == "*"

    @pytest.mark.parametrize("policy_json", [
        {
            "uid": "1",
            "description": "Policy create error test: Unknown condition 'Eqs'",
            "rules": {
                "subject": {"$.uid": {"condition": "Eqs", "value": 1.0}},
                "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
                "action": {},
                "context": {}
            },
            "targets": {
                "subject_id": ["abc", "a*"],
                "resource_id": ["123"],
                'action_id': '*'
            },
            "effect": "deny",
            "priority": 0
        },
        {
            "uid": "1",
            "description": "Policy create error test: Invalid rules",
            "rules": {
                "subject": None,
                "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
                "action": {},
                "context": {}
            },
            "targets": {
                "subject_id": ["abc", "a*"],
                "resource_id": ["123"],
                'action_id': '*'
            },
            "effect": "deny",
            "priority": 0
        },
        {
            "uid": "1",
            "description": "Policy create error test: Invalid targets",
            "rules": {
                "subject": None,
                "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
                "action": {},
                "context": {}
            },
            "targets": {
                "subject_id": None,
                "resource_id": ["123"],
                'action_id': '*'
            },
            "effect": "deny",
            "priority": 0
        },
        {
            "uid": "1",
            "description": "Policy create error test: Invalid effect 'test'",
            "rules": {
                "subject": None,
                "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
                "action": {},
                "context": {}
            },
            "targets": {
                "subject_id": ["abc", "a*"],
                "resource_id": ["123"],
                'action_id': '*'
            },
            "effect": "test",
            "priority": 0
        },
        {
            "uid": "1",
            "description": "Policy create error test: Invalid priority 'test'",
            "rules": {
                "subject": None,
                "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
                "action": {},
                "context": {}
            },
            "targets": {
                "subject_id": ["abc", "a*"],
                "resource_id": ["123"],
                'action_id': '*'
            },
            "effect": "test",
            "priority": -1
        },
    ])
    def test_create_policy_error(self, policy_json):
        with pytest.raises(PolicyCreateError):
            Policy.from_json(policy_json)

    def test_allow_access(self):
        policy_json = {
            "uid": "a",
            "description": "Policy create test",
            "rules": {
                "subject": {"$.uid": {"condition": "Eq", "value": 1.0}},
                "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
                "action": {},
                "context": {}
            },
            "targets": {
                "subject_id": ["abc", "a*"],
                "resource_id": ["123"],
                'action_id': '*'
            },
            "effect": "deny",
            "priority": 0
        }
        policy = Policy.from_json(policy_json)
        assert not policy.is_allowed
        policy.effect = "allow"
        assert policy.is_allowed

    @pytest.mark.parametrize("desc, policy_json, request_json, result", [
        (
                "Policy 1",
                {
                    "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
                    "description": "Block user 'Max'",
                    "rules": {
                        "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
                    },
                    "targets": {},
                    "effect": "deny"
                },
                {
                    "subject": {
                        "id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb",
                        "attributes": {"name": "Max"}
                    },
                    "resource": {"id": "resource::9ce7e474-b16f-4fb1-980e-bd1462bcd5a1"},
                    "action": {"id": "action::GET"},
                    "context": {}
                },
                True
        ),
        (
                "Policy 2",
                {
                    "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
                    "description": "Block user 'Max'",
                    "rules": {
                        "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
                    },
                    "targets": {},
                    "effect": "deny"
                },
                {
                    "subject": {
                        "id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb",
                        "attributes": {"name": "Carl"}
                    },
                    "resource": {"id": "resource::9ce7e474-b16f-4fb1-980e-bd1462bcd5a1"},
                    "action": {"id": "action::GET"},
                    "context": {}
                },
                False
        ),
        (
                "Policy 3",
                {
                    "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
                    "description": "Block user 'Max'",
                    "rules": {
                        "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
                    },
                    "targets": {
                        "subject_id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb"
                    },
                    "effect": "deny"
                },
                {
                    "subject": {
                        "id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb",
                        "attributes": {"name": "Max"}
                    },
                    "resource": {"id": "resource::9ce7e474-b16f-4fb1-980e-bd1462bcd5a1"},
                    "action": {"id": "action::GET"},
                    "context": {}
                },
                True
        ),
        (
                "Policy 4",
                {
                    "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
                    "description": "Block user 'Max'",
                    "rules": {
                        "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
                    },
                    "targets": {
                        "subject_id": "user::b90b2998-*"
                    },
                    "effect": "deny"
                },
                {
                    "subject": {
                        "id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb",
                        "attributes": {"name": "Max"}
                    },
                    "resource": {"id": "resource::9ce7e474-b16f-4fb1-980e-bd1462bcd5a1"},
                    "action": {"id": "action::GET"},
                    "context": {}
                },
                True
        ),
        (
                "Policy 5",
                {
                    "uid": "a381fdd3-b73a-4858-a57b-94085628b0f1",
                    "description": "Block user 'Max'",
                    "rules": {
                        "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
                    },
                    "targets": {
                        "subject_id": "user::b90b2998-9e1b"
                    },
                    "effect": "deny"
                },
                {
                    "subject": {
                        "id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb",
                        "attributes": {"name": "Max"}
                    },
                    "resource": {"id": "resource::9ce7e474-b16f-4fb1-980e-bd1462bcd5a1"},
                    "action": {"id": "action::GET"},
                    "context": {}
                },
                False
        ),
        (
                "Policy 6",
                {
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
                },
                {
                    "subject": {
                        "id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb",
                        "attributes": {"name": "Max"}
                    },
                    "resource": {"id": "resource::9ce7e474-b16f-4fb1-980e-bd1462bcd5a1"},
                    "action": {"id": "action::GET"},
                    "context": {"ip": "192.168.2.10"}
                },
                True
        ),
        (
                "Policy 7",
                {
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
                },
                {
                    "subject": {
                        "id": "user::b90b2998-9e1b-4ac5-a743-b060b2634dbb",
                        "attributes": {"name": "Max"}
                    },
                    "resource": {"id": "resource::9ce7e474-b16f-4fb1-980e-bd1462bcd5a1"},
                    "action": {"id": "action::GET"},
                    "context": {"ip": "192.168.1.10"}
                },
                False
        ),
    ])
    def test_fits(self, desc, policy_json, request_json, result):
        request = Request.from_json(request_json)
        policy = Policy.from_json(policy_json)
        assert policy.fits(request) == result
