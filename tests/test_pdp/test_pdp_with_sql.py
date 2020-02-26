"""
    PDP tests with SQL storage
"""

import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from py_abac.pdp import PDP, EvaluationAlgorithm
from py_abac.policy import Policy
from py_abac.provider.base import AttributeProvider
from py_abac.request import Request
from py_abac.storage.sql import SQLMigrationSet, SQLStorage
from py_abac.storage.sql.model import Base
from ..test_storage.test_sql import create_test_sql_engine

SUBJECT_IDS = {"Max": "user:1", "Nina": "user:2", "Ben": "user:3", "Henry": "user:4"}
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
        "targets": {"subject_id": SUBJECT_IDS["Max"]},
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
        "targets": {"subject_id": SUBJECT_IDS["Max"]},
        "priority": 0
    },
    {
        "uid": "4",
        "description": "No rules and targets. Policy should not match any authorization request.",
        "effect": "deny",
        "rules": {
            "subject": [],
            "resource": [],
            "action": [],
            "context": [],
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
        "targets": {"subject_id": SUBJECT_IDS["Nina"]},
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
        "targets": {"subject_id": SUBJECT_IDS["Nina"]},
        "priority": 0
    },
    {
        "uid": "7",
        "description": "Ben is allowed to print any resource when logged in with gmail account",
        "effect": "allow",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Ben"},
                        "$.email": {"condition": "Equals", "value": "ben@gmail.com"}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
            "action": {"$.method": {"condition": "Equals", "value": "print"}},
            "context": {}
        },
        "targets": {"subject_id": SUBJECT_IDS["Ben"]},
        "priority": 0
    },
    {
        "uid": "8",
        "description": "All users with employee role are blocked to access confidential documents.",
        "effect": "deny",
        "rules": {
            "subject": {"$.roles": {"condition": "AnyIn", "values": ["employee"]}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": "doc:confidential:.*"}},
            "action": {"$.method": {"condition": "RegexMatch", "value": ".*"}},
            "context": {}
        },
        "targets": {},
        "priority": 0
    },
    {
        "uid": "9",
        "description": "All users with manager role are allowed view access to sales confidential documents.",
        "effect": "allow",
        "rules": {
            "subject": {"$.roles": {"condition": "AnyIn", "values": ["manager"]}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": "doc:confidential:sales:.*"}},
            "action": {"$.method": {"condition": "Equals", "value": "get"}},
            "context": {}
        },
        "targets": {},
        "priority": 1
    },
]


class EmailsAttributeProvider(AttributeProvider):

    def get_attribute_value(self, ace: str, attribute_path: str, ctx):
        if ace == "subject" and attribute_path == "$.email":
            if ctx.get_attribute_value(ace, "$.name") == "Ben":
                return "ben@gmail.com"


@pytest.fixture
def session():
    engine = create_test_sql_engine()
    Base.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    Base.metadata.drop_all(engine)


@pytest.fixture
def st(session):
    storage = SQLStorage(scoped_session=session)
    migration_set = SQLMigrationSet(storage)
    migration_set.up()
    for policy_json in POLICIES:
        storage.add(Policy.from_json(policy_json))
    yield storage
    migration_set.down()
    session.remove()


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
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max is allowed to update anything, even empty one',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max, but not max is allowed to update anything (case-sensitive comparison)',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even if no resource is given',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even an empty resource',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 matches and has allow-effect',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 matches - Henry is listed in the allowed subjects regexp',
            {
                "subject": {"id": SUBJECT_IDS["Henry"], "attributes": {"name": "Henry"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 does not match - context was not found (misspelled)',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"IP": "127.0.0.1"}
            },
            False,
    ),
    (
            'Policy #1 does not match - context is missing',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 does not match - context says IP is not in the allowed range',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "0.0.0.0"}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, but subjects does not match',
            {
                "subject": {"id": "user:10", "attributes": {"name": "Sarah"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, subject is Nina, but resource-name is not digits',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "abcd"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 should match',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Policy #5 and #6 should match - usage of "id" in context. Policy #6 overrides.',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"id": "3fkap-bmvci-rmvp0"}
            },
            False,
    ),
    (
            'Policy #5 should match and not #6 - usage of different context',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"name": "test"}
            },
            True,
    ),
    (
            'Ben is allowed to print anything when logged in with gmail',
            {
                "subject": {"id": SUBJECT_IDS["Ben"], "attributes": {"name": "Ben"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            True,
    ),
    (
            'Ben is not allowed to print anything when logged in with yahoo',
            {
                "subject": {"id": SUBJECT_IDS["Ben"], "attributes": {"name": "Ben", "email": "ben@yahoo.com"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'A user with employee role is not allowed to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["employee"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            False,
    ),
    (
            'A user with manager role is allowed to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            True,
    ),
    (
            'A user with manager role is not allowed to view other classified documents',
            {
                "subject": {"id": "", "attributes": {"roles": ["manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:products:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            False,
    ),
    (
            'Deny override algorithm blocks user with both manager and employee roles '
            'to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["employee", "manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            False,
    ),
])
def test_is_allowed_deny_overrides(st, desc, request_json, should_be_allowed):
    pdp = PDP(st, EvaluationAlgorithm.DENY_OVERRIDES, [EmailsAttributeProvider()])
    request = Request.from_json(request_json)
    assert should_be_allowed == pdp.is_allowed(request)


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
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max is allowed to update anything, even empty one',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max, but not max is allowed to update anything (case-sensitive comparison)',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even if no resource is given',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even an empty resource',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 matches and has allow-effect',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 matches - Henry is listed in the allowed subjects regexp',
            {
                "subject": {"id": SUBJECT_IDS["Henry"], "attributes": {"name": "Henry"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 does not match - context was not found (misspelled)',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"IP": "127.0.0.1"}
            },
            False,
    ),
    (
            'Policy #1 does not match - context is missing',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 does not match - context says IP is not in the allowed range',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "0.0.0.0"}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, but subjects does not match',
            {
                "subject": {"id": "user:10", "attributes": {"name": "Sarah"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, subject is Nina, but resource-name is not digits',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "abcd"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 should match',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Policy #5 and #6 should match - usage of "id" in context. Policy #5 overrides.',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"id": "3fkap-bmvci-rmvp0"}
            },
            True,
    ),
    (
            'Policy #5 should match and not #6 - usage of different context',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"name": "test"}
            },
            True,
    ),
    (
            'Ben is allowed to print anything when logged in with gmail',
            {
                "subject": {"id": SUBJECT_IDS["Ben"], "attributes": {"name": "Ben"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            True,
    ),
    (
            'Ben is not allowed to print anything when logged in with yahoo',
            {
                "subject": {"id": SUBJECT_IDS["Ben"], "attributes": {"name": "Ben", "email": "ben@yahoo.com"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'A user with employee role is not allowed to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["employee"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            False,
    ),
    (
            'A user with manager role is allowed to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            True,
    ),
    (
            'A user with manager role is not allowed to view other classified documents',
            {
                "subject": {"id": "", "attributes": {"roles": ["manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:products:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            False,
    ),
    (
            'Allow override algorithm allows user with both manager and employee roles '
            'to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["employee", "manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            True,
    ),
])
def test_is_allowed_allow_overrides(st, desc, request_json, should_be_allowed):
    pdp = PDP(st, EvaluationAlgorithm.ALLOW_OVERRIDES, [EmailsAttributeProvider()])
    request = Request.from_json(request_json)
    assert should_be_allowed == pdp.is_allowed(request)


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
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max is allowed to update anything, even empty one',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Max, but not max is allowed to update anything (case-sensitive comparison)',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even if no resource is given',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Max is not allowed to print anything, even an empty resource',
            {
                "subject": {"id": SUBJECT_IDS["Max"], "attributes": {"name": "Max"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 matches and has allow-effect',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 matches - Henry is listed in the allowed subjects regexp',
            {
                "subject": {"id": SUBJECT_IDS["Henry"], "attributes": {"name": "Henry"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {"ip": "127.0.0.1"}
            },
            True,
    ),
    (
            'Policy #1 does not match - context was not found (misspelled)',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"IP": "127.0.0.1"}
            },
            False,
    ),
    (
            'Policy #1 does not match - context is missing',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #1 does not match - context says IP is not in the allowed range',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "delete"}},
                "context": {"ip": "0.0.0.0"}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, but subjects does not match',
            {
                "subject": {"id": "user:10", "attributes": {"name": "Sarah"}},
                "resource": {"id": "", "attributes": {"name": "myrn:example.com:resource:123"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 does not match - action is update, subject is Nina, but resource-name is not digits',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "abcd"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            False,
    ),
    (
            'Policy #5 should match',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {}
            },
            True,
    ),
    (
            'Policy #5 and #6 should match - usage of "id" in context. Policy #6 overrides.',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"id": "3fkap-bmvci-rmvp0"}
            },
            False,
    ),
    (
            'Policy #5 should match and not #6 - usage of different context',
            {
                "subject": {"id": SUBJECT_IDS["Nina"], "attributes": {"name": "Nina"}},
                "resource": {"id": "", "attributes": {"name": "00678"}},
                "action": {"id": "", "attributes": {"method": "update"}},
                "context": {"name": "test"}
            },
            True,
    ),
    (
            'Ben is allowed to print anything when logged in with gmail',
            {
                "subject": {"id": SUBJECT_IDS["Ben"], "attributes": {"name": "Ben"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            True,
    ),
    (
            'Ben is not allowed to print anything when logged in with yahoo',
            {
                "subject": {"id": SUBJECT_IDS["Ben"], "attributes": {"name": "Ben", "email": "ben@yahoo.com"}},
                "resource": {"id": "", "attributes": {"name": ""}},
                "action": {"id": "", "attributes": {"method": "print"}},
                "context": {}
            },
            False,
    ),
    (
            'A user with employee role is not allowed to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["employee"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            False,
    ),
    (
            'A user with manager role is allowed to view classified documents for sales',
            {
                "subject": {"id": "", "attributes": {"roles": ["manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            True,
    ),
    (
            'A user with manager role is not allowed to view other classified documents',
            {
                "subject": {"id": "", "attributes": {"roles": ["manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:products:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            False,
    ),
    (
            'Highest priority algorithm allows user with both manager and employee roles '
            'to view classified documents for sales. Policy #9 applies due to higher priority.',
            {
                "subject": {"id": "", "attributes": {"roles": ["employee", "manager"]}},
                "resource": {"id": "", "attributes": {"name": "doc:confidential:sales:I3462"}},
                "action": {"id": "", "attributes": {"method": "get"}},
                "context": {}
            },
            True,
    ),
])
def test_is_allowed_highest_priority(st, desc, request_json, should_be_allowed):
    pdp = PDP(st, EvaluationAlgorithm.HIGHEST_PRIORITY, [EmailsAttributeProvider()])
    request = Request.from_json(request_json)
    assert should_be_allowed == pdp.is_allowed(request)


def test_pdp_create_error(st):
    with pytest.raises(TypeError):
        PDP(None)
    with pytest.raises(TypeError):
        PDP(st, None)
    with pytest.raises(TypeError):
        PDP(st, EvaluationAlgorithm.DENY_OVERRIDES, [None])


def test_is_allowed_error(st):
    g = PDP(st)
    with pytest.raises(TypeError):
        g.is_allowed(None)
