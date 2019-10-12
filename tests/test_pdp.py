"""
    PDP tests
"""

import pytest
from pymongo import MongoClient

from py_abac.pdp import PDP, EvaluationAlgorithm
from py_abac.policy import Policy
from py_abac.request import Request
from py_abac.storage.mongo import MongoStorage, MongoMigrationSet

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
DB_NAME = 'db_test'
COLLECTION = 'policies_test'
POLICIES = [
    {
        "uid": "1",
        "description": "Max, Nina, Ben, Henry are allowed to create, delete, get "
                       "the resources only if the client IP matches.",
        "effect": "allow",
        "rules": {
            "subject": [{"$.name": {"condition": "Equals", "value": "Max"}},
                        {"$.name": {"condition": "Equals", "value": "Nina"}},
                        {"$.name": {"condition": "AnyOf",
                                    "values": [{"condition": "Equals", "value": "Ben"},
                                               {"condition": "Equals", "value": "Henry"}]}}],
            "resource": {"$.name": {"condition": "AnyOf",
                                    "values": [{"condition": "Equals", "value": "myrn:example.com:resource:123"},
                                               {"condition": "Equals", "value": "myrn:example.com:resource:345"},
                                               {"condition": "RegexMatch", "value": "myrn:something:foo:.*"}]}},
            "action": [{"$.method": {"condition": "AnyOf",
                                     "values": [{"condition": "Equals", "value": "create"},
                                                {"condition": "Equals", "value": "delete"}]}},
                       {"$.method": {"condition": "Equals", "value": "get"}}],
            "context": {"$.ip": {"condition": "CIDR", "value": "127.0.0.1/32"}}
        },
        "targets": {},
        "priority": 0
    },
    {
        "uid": "2",
        "description": "Allows Max to update any resource",
        "effect": "allow",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
            "action": {"$.method": {"condition": "Equals", "value": "update"}},
            "context": {}
        },
        "targets": {},
        "priority": 0
    },
    {
        "uid": "3",
        "description": "Max is not allowed to print any resource",
        "effect": "deny",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
            "action": {"$.method": {"condition": "Equals", "value": "print"}},
            "context": {}
        },
        "targets": {},
        "priority": 0
    },
    {
        "uid": "4",
        "description": "No rules and targets. Policy should not match any authorization request.",
        "effect": "deny",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
            "action": {"$.method": {"condition": "Equals", "value": "print"}},
            "context": {}
        },
        "targets": {}
    },
    {
        "uid": "5",
        "description": "Allows Nina to update any resources that have only digits",
        "effect": "allow",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Nina"}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": r"\d+"}},
            "action": {"$.method": {"condition": "Equals", "value": "update"}},
            "context": {}
        },
        "targets": {},
        "priority": 0
    },
    {
        "uid": "6",
        "description": "Prevent Nina to update any resources when ID is passed in context",
        "effect": "deny",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Nina"}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": r"\d+"}},
            "action": {"$.method": {"condition": "Equals", "value": "update"}},
            "context": {"$.id": {"condition": "Exists"}}
        },
        "targets": {},
        "priority": 0
    }
]


def create_client():
    return MongoClient(MONGO_HOST, MONGO_PORT)


@pytest.fixture
def st():
    client = create_client()
    storage = MongoStorage(client, DB_NAME, collection=COLLECTION)
    migration_set = MongoMigrationSet(storage)
    migration_set.up()
    for policy_json in POLICIES:
        storage.add(Policy.from_json(policy_json))
    yield storage
    migration_set.down()
    client[DB_NAME][COLLECTION].drop()
    client.close()


@pytest.mark.parametrize('desc, request_json, should_be_allowed', [
    (
            'Empty inquiry carries no information, so nothing is allowed, even empty Policy #4',
            {
                "subject": {"id": ""},
                "resource": {"id": ""},
                "action": {"id": ""},
                "context": {}
            },
            False,
    ),
    (
            'Max is allowed to update anything',
            {
                "subject": {"id": "", "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max is allowed to update anything, even empty one',
            {
                "subject": {"id": "", "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max, but not max is allowed to update anything (case-sensitive comparison)',
            {
                "subject": {"id": "", "attributes": {"name": "max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything',
            {
                "subject": {"id": "", "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even if no resource is given',
            {
                "subject": {"id": "", "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even an empty resource',
            {
                "subject": {"id": "", "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 matches and has allow-effect',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 matches - Henry is listed in the allowed subjects regexp',
            {
                "subject": {"id": "", "attributes": {"name": "Henry"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 does not match - context was not found (misspelled)',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"IP": "127.0.0.1"}
            },
            False,
    ),
    (
            'Policy #1 does not match - context is missing',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 does not match - context says IP is not in the allowed range',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "0.0.0.0"}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, but subjects does not match',
            {
                "subject": {"id": "", "attributes": {"name": "Sarah"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, subject is Nina, but resource-name is not digits',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "abcd"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 should match',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Policy #6 should match - usage of "id" in context',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"id": "3fkap-bmvci-rmvp0"}
            },
            False,
    ),
    (
            'Policy #6 should match - usage of different context',
            {
                "subject": {"id": "", "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"name": "test"}
            },
            True,
    ),
])
def test_is_allowed_deny_overrides(st, desc, request_json, should_be_allowed):
    pdp = PDP(st, EvaluationAlgorithm.DENY_OVERRIDES)
    request = Request.from_json(request_json)
    assert should_be_allowed == pdp.is_allowed(request)


def test_guard_create_error(st):
    with pytest.raises(TypeError):
        PDP(None)
    with pytest.raises(TypeError):
        PDP(st, None)


def test_is_allowed_error(st):
    g = PDP(st)
    with pytest.raises(TypeError):
        g.is_allowed(None)
