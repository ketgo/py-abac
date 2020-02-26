"""
    MongoDB storage test
"""

import uuid

import pytest

from py_abac.exceptions import PolicyExistsError
from py_abac.policy import Policy
from py_abac.policy.conditions.numeric import Eq
from py_abac.policy.conditions.string import Equals
from py_abac.request import Request
from py_abac.storage.mongo import MongoStorage
from . import create_client

DB_NAME = 'db_test'
COLLECTION = 'policies_test'


@pytest.fixture
def st():
    client = create_client()
    storage = MongoStorage(client, DB_NAME, collection=COLLECTION)
    yield storage
    client[DB_NAME][COLLECTION].delete_many({})
    client.close()


def test_add(st):
    policy_json = {
        "uid": "1",
        "description": "Policy create test 1",
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
    st.add(policy)
    assert "1" == st.get('1').uid
    assert "Policy create test 1" == st.get('1').description

    policy_json = {
        "uid": "2",
        "description": "Policy create test 2",
        "rules": {
            "subject": {"$.uid": {"condition": "Eq", "value": 1.0}},
            "resource": [{"$.name": {"condition": "Equals", "value": "test", "case_insensitive": False}}],
            "action": [{"$.method": {"condition": "Equals", "value": "GET"}},
                       {"$.method": {"condition": "Equals", "value": "POST"}}],
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
    st.add(policy)
    assert '2' == st.get('2').uid
    assert 2 == len(st.get('2').rules.action)
    assert 1 == len(st.get('2').rules.subject)
    assert isinstance(st.get('2').rules.subject["$.uid"], Eq)
    assert 1 == len(st.get('2').rules.resource)
    assert isinstance(st.get('2').rules.resource[0]['$.name'], Equals)
    assert 'test' == st.get('2').rules.resource[0]['$.name'].value
    assert ["abc", "a*"] == st.get('2').targets.subject_id


def test_policy_create_existing(st):
    st.add(Policy.from_json({"uid": "1", "rules": {}, "targets": {}, "effect": "deny"}))
    with pytest.raises(PolicyExistsError):
        st.add(Policy.from_json({"uid": "1", "rules": {}, "targets": {}, "effect": "deny"}))


def test_get(st):
    st.add(Policy.from_json({"uid": "1", "rules": {}, "targets": {}, "effect": "deny"}))
    st.add(Policy.from_json({"uid": "2", "description": "some text", "rules": {}, "targets": {}, "effect": "deny"}))
    assert isinstance(st.get('1'), Policy)
    assert '1' == st.get('1').uid
    assert '2' == st.get('2').uid
    assert 'some text' == st.get('2').description


@pytest.mark.parametrize('limit, offset, result', [
    (500, 0, 200),
    (101, 1, 101),
    (500, 50, 150),
    (200, 0, 200),
    (200, 1, 199),
    (199, 0, 199),
    (200, 50, 150),
    # TODO: Fix - result should be 0
    (0, 0, 200),
    (1, 0, 1),
    (5, 4, 5),
    (200, 300, 0),
])
def test_get_all(st, limit, offset, result):
    for i in range(200):
        st.add(Policy.from_json({"uid": str(i), "rules": {}, "targets": {}, "effect": "deny"}))
    policies = list(st.get_all(limit, offset))
    assert result == len(policies)


def test_get_all_check_policy_properties(st):
    st.add(Policy.from_json({"uid": "1", "description": "foo", "rules": {}, "targets": {}, "effect": "deny"}))
    policies = list(st.get_all(100, 0))
    assert 1 == len(policies)
    assert '1' == policies[0].uid
    assert 'foo' == policies[0].description


def test_get_all_with_incorrect_args(st):
    with pytest.raises(ValueError) as e:
        list(st.get_all(-1, 90))
    assert "Limit can't be negative" == str(e.value)

    with pytest.raises(ValueError) as e:
        list(st.get_all(0, -34))
    assert "Offset can't be negative" == str(e.value)


@pytest.mark.parametrize("request_json, num", [
    ({
         "subject": {"id": "a"},
         "resource": {"id": str(uuid.uuid4())},
         "action": {"id": str(uuid.uuid4())}
     }, 1),
    ({
         "subject": {"id": "ab"},
         "resource": {"id": str(uuid.uuid4())},
         "action": {"id": str(uuid.uuid4())}
     }, 3),
    ({
         "subject": {"id": "abc"},
         "resource": {"id": str(uuid.uuid4())},
         "action": {"id": str(uuid.uuid4())}
     }, 3),
    ({
         "subject": {"id": "acb"},
         "resource": {"id": str(uuid.uuid4())},
         "action": {"id": str(uuid.uuid4())}
     }, 2),
    ({
         "subject": {"id": "axc"},
         "resource": {"id": str(uuid.uuid4())},
         "action": {"id": str(uuid.uuid4())}
     }, 1),
])
def test_find_for_target(st, request_json, num):
    st.add(Policy.from_json({"uid": "1",
                             "rules": {},
                             "targets": {},
                             "effect": "deny"}))
    st.add(Policy.from_json({"uid": "2",
                             "rules": {},
                             "targets": {"subject_id": "ab*"},
                             "effect": "deny"}))
    st.add(Policy.from_json({"uid": "3",
                             "rules": {},
                             "targets": {"subject_id": "a*b"},
                             "effect": "deny"}))
    st.add(Policy.from_json({"uid": "4",
                             "rules": {},
                             "targets": {"subject_id": "ab*c"},
                             "effect": "deny"}))

    request = Request.from_json(request_json)
    found = st.get_for_target(request._subject_id, request._resource_id, request._action_id)
    found = list(found)
    assert num == len(found)


def test_update(st):
    policy = Policy.from_json({"uid": "1", "rules": {}, "targets": {}, "effect": "deny"})
    st.add(policy)
    assert '1' == st.get('1').uid
    assert '' is st.get('1').description
    policy.description = 'foo'
    st.update(policy)
    assert '1' == st.get('1').uid
    assert 'foo' == st.get('1').description
    p = Policy.from_json({"uid": "2",
                          "description": "foo",
                          "rules": {},
                          "targets": {},
                          "effect": "deny"})
    st.add(p)
    assert '2' == st.get('2').uid
    p = Policy.from_json({"uid": "2",
                          "description": "foo",
                          "rules": {"action": {"$.method": {"condition": "Equals", "value": "get"}}},
                          "targets": {},
                          "effect": "deny"})
    st.update(p)
    assert 1 == len(st.get('2').rules.action)
    assert 'get' == st.get('2').rules.action['$.method'].value


def test_delete(st):
    policy = Policy.from_json({"uid": "1", "rules": {}, "targets": {}, "effect": "deny"})
    st.add(policy)
    assert '1' == st.get('1').uid
    st.delete('1')
    assert None is st.get('1')
