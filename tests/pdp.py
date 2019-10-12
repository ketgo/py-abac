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
        "description": """
        Max, Nina, Ben, Henry are allowed to create, delete, get the resources
        only if the client IP matches.
        """,
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
    Policy(
        uid='2',
        description='Allows Max to update any resource',
        effect=ALLOW_ACCESS,
        subjects=[{"$.name": Equals('Max')}],
        actions=[{"$.method": Equals('update')}],
        resources=[{"$.name": RegexMatch('.*')}],
    ),
    Policy(
        uid='3',
        description='Max is not allowed to print any resource',
        effect=DENY_ACCESS,
        subjects=[{"$.name": Equals('Max')}],
        actions=[{"$.method": Equals('print')}],
        resources=[{"$.name": RegexMatch('.*')}],
    ),
    Policy(
        uid='4'
    ),
    Policy(
        uid='5',
        description='Allows Nina to update any resources that have only digits',
        effect=ALLOW_ACCESS,
        subjects=[{"$.name": Equals('Nina')}],
        actions=[{"$.method": Equals('update')}],
        resources=[{"$.name": RegexMatch(r'\d+')}],
    ),
    Policy(
        uid='6',
        description='Allows Nina to update any resources that have only digits.',
        effect=ALLOW_ACCESS,
        subjects=[{"$.name": Equals('Nina')}],
        actions=[{"$.method": Equals('update')}, {"$.method": Equals('read')}],
        resources=[{'$.id': RegexMatch(r'\d+'), '$.magazine': RegexMatch(r'[\d\w]+')}],
    ),
    Policy(
        uid='7',
        description='Prevent Nina to update any resources when ID is passed in context',
        effect=DENY_ACCESS,
        subjects=[{"$.name": Equals('Nina')}],
        actions=[{"$.method": Equals('update')}, {"$.method": Equals('read')}],
        resources=[{'$.id': RegexMatch(r'\d+'), '$.magazine': RegexMatch(r'[\d\w]+')}],
        context={'$.id': Exists()}
    ),
]


def create_client():
    return MongoClient(MONGO_HOST, MONGO_PORT)


@pytest.fixture
def st():
    client = create_client()
    storage = MongoStorage(client, DB_NAME, collection=COLLECTION)
    migration_set = MongoMigrationSet(storage)
    migration_set.up()
    for p in POLICIES:
        storage.add(p)
    yield storage
    migration_set.down()
    client[DB_NAME][COLLECTION].delete_many({})
    client.close()


@pytest.mark.parametrize('desc, request_json, should_be_allowed', [
    (
            'Empty inquiry carries no information, so nothing is allowed, even empty Policy #4',
            Inquiry(),
            False,
    ),
    (
            'Max is allowed to update anything',
            Inquiry(
                subject={'name': 'Max'},
                resource={'name': 'myrn:example.com:resource:123'},
                action={'method': 'update'}
            ),
            True,
    ),
    (
            'Max is allowed to update anything, even empty one',
            Inquiry(
                subject={'name': 'Max'},
                resource={'name': ''},
                action={'method': 'update'}
            ),
            True,
    ),
    (
            'Max, but not max is allowed to update anything (case-sensitive comparison)',
            Inquiry(
                subject={'name': 'max'},
                resource={'name': 'myrn:example.com:resource:123'},
                action={'method': 'update'}
            ),
            False,
    ),
    (
            'Max is not allowed to print anything',
            Inquiry(
                subject={'name': 'Max'},
                resource={'name': 'myrn:example.com:resource:123'},
                action={'method': 'print'},
            ),
            False,
    ),
    (
            'Max is not allowed to print anything, even if no resource is given',
            Inquiry(
                subject={'name': 'Max'},
                action={'method': 'print'}
            ),
            False,
    ),
    (
            'Max is not allowed to print anything, even an empty resource',
            Inquiry(
                subject={'name': 'Max'},
                action={'method': 'print'},
                resource={'name': ''}
            ),
            False,
    ),
    (
            'Policy #1 matches and has allow-effect',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'ip': '127.0.0.1'}
            ),
            True,
    ),
    (
            'Policy #1 matches - Henry is listed in the allowed subjects regexp',
            Inquiry(
                subject={'name': 'Henry'},
                action={'method': 'get'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'ip': '127.0.0.1'}
            ),
            True,
    ),
    (
            'Policy #1 does not match - context was not found (misspelled)',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'IP': '127.0.0.1'}
            ),
            False,
    ),
    (
            'Policy #1 does not match - context is missing',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={}
            ),
            False,
    ),
    (
            'Policy #1 does not match - context says IP is not in the allowed range',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'ip': '0.0.0.0'}
            ),
            False,
    ),
    (
            'Policy #5 does not match - action is update, but subjects does not match',
            Inquiry(
                subject={'name': 'Sarah'},
                action={'method': 'update'},
                resource={'name': '88'},
            ),
            False,
    ),
    (
            'Policy #5 does not match - action is update, subject is Nina, but resource-name is not digits',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'update'},
                resource={'name': 'abcd'},
            ),
            False,
    ),
    (
            'Policy #6 does not match - Inquiry has wrong format for resource',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'update'},
                resource={'name': 'abcd'},
            ),
            False,
    ),
    (
            'Policy #6 does not match - Inquiry has string ID for resource',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': 'abcd'},
            ),
            False,
    ),
    (
            'Policy #6 should match',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'update'},
                resource={'id': '00678', 'magazine': 'Playboy1'},
            ),
            True,
    ),
    (
            'Policy #6 should not match - usage of inappropriate resource ID',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': 'abc', 'magazine': 'Playboy1'},
            ),
            False,
    ),
    (
            'Policy #7 should match - usage of inappropriate context',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': '00678', 'magazine': 'Playboy1'},
                context={'id': 'Nina'}
            ),
            False,
    ),
    (
            'Policy #7 should not match - usage of different context',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': '00678', 'magazine': 'Playboy1'},
                context={'name': 'Nina'}
            ),
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
