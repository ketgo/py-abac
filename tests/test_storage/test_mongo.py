"""
    Test memory storage
"""

import pytest
from pymongo import MongoClient

from py_abac.common.constants import DEFAULT_POLICY_COLLECTION
from py_abac.common.exceptions import PolicyExistsError
from py_abac.conditions.logic import Or
from py_abac.conditions.others import Exists
from py_abac.conditions.string import Equals
from py_abac.inquiry import Inquiry
from py_abac.policy import Policy
from py_abac.storage.mongo import MongoStorage

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
DB_NAME = 'db_test'
COLLECTION = 'policies_test'


def create_client():
    return MongoClient(MONGO_HOST, MONGO_PORT)


@pytest.fixture
def st():
    client = create_client()
    yield MongoStorage(client, DB_NAME, collection=COLLECTION)
    client[DB_NAME][COLLECTION].delete_many({})
    client.close()


def test_add(st):
    st.add(Policy('1', description='foo'))
    assert '1' == st.get('1').uid
    assert 'foo' == st.get('1').description
    st.add(Policy('2',
                  actions=[{"$.method": Equals("delete")},
                           {"$.method": Or(Equals("get"), Equals("put"))}],
                  subjects=[{"$.name": Exists()}],
                  resources=[{'$.books': Equals('Harry')}]))
    assert '2' == st.get('2').uid
    assert 2 == len(st.get('2').actions)
    assert 1 == len(st.get('2').subjects)
    assert isinstance(st.get('2').subjects[0]["$.name"], Exists)
    assert 1 == len(st.get('2').resources)
    assert isinstance(st.get('2').resources[0]['$.books'], Equals)
    assert 'Harry' == st.get('2').resources[0]['$.books'].value


def test_policy_create_existing(st):
    st.add(Policy('1', description='foo'))
    with pytest.raises(PolicyExistsError):
        st.add(Policy('1', description='bar'))


def test_get(st):
    st.add(Policy('1'))
    st.add(Policy('2', description='some text'))
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
    (0, 0, 200),
    (1, 0, 1),
    (5, 4, 5),
    (200, 300, 0),
])
def test_get_all(st, limit, offset, result):
    for i in range(200):
        st.add(Policy(str(i)))
    policies = list(st.get_all(limit, offset))
    assert result == len(policies)


def test_get_all_check_policy_properties(st):
    st.add(Policy('1', description='foo'))
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


def test_find_for_inquiry(st):
    st.add(Policy('1', subjects=[{"$.name": Equals('max')}, {"$.name": Equals('bob')}]))
    st.add(Policy('2', subjects=[{"$.name": Equals('sam')}, {"$.name": Equals('nina')}]))
    st.add(Policy('3', subjects=[{"$.name": Equals('max')}, {"$.name": Equals('bob')}]))
    inquiry = Inquiry(subject={"name": 'sam'}, action={"method": 'get'}, resource={"name": 'books'})
    found = st.get_for_inquiry(inquiry)
    found = list(found)
    assert 3 == len(found)
    assert all(x.collection == DEFAULT_POLICY_COLLECTION for x in found)


def test_update(st):
    policy = Policy('1')
    st.add(policy)
    assert '1' == st.get('1').uid
    assert '' is st.get('1').description
    policy.description = 'foo'
    st.update(policy)
    assert '1' == st.get('1').uid
    assert 'foo' == st.get('1').description
    p = Policy('2', actions=[{'$.name': Exists()}])
    st.add(p)
    assert '2' == st.get('2').uid
    p.actions = [{"$.name": Equals('get')}]
    st.update(p)
    assert 1 == len(st.get('2').actions)
    assert 'get' == st.get('2').actions[0]['$.name'].value


def test_delete(st):
    policy = Policy('1')
    st.add(policy)
    assert '1' == st.get('1').uid
    st.delete('1')
    assert None is st.get('1')
    st.delete('1000000')
