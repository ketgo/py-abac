"""
    SQL storage tests
"""

import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from py_abac.policy import Policy
from py_abac.policy.conditions.numeric import Eq
from py_abac.policy.conditions.string import Equals
from py_abac.storage.sql import SQLStorage, SQLMigrationSet
from py_abac.storage.sql.model import Base
from . import create_test_sql_engine


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
    yield storage
    migration_set.down()
    session.remove()


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
