"""
    Policy tests
"""

import uuid

import pytest

from pyabac.common.constants import DEFAULT_POLICY_COLLECTION, DENY_ACCESS, ALLOW_ACCESS
from pyabac.common.exceptions import PolicyCreationError
from pyabac.conditions.string import Equals
from pyabac.policy import Policy


class TestPolicy(object):

    def test_to_json(self):
        uid = uuid.uuid4()
        policy = Policy(uid=uid,
                        description="test",
                        subjects=[{"$.name": Equals("pyabac")}],
                        resources=[],
                        actions=[],
                        context={},
                        effect=DENY_ACCESS,
                        collection=DEFAULT_POLICY_COLLECTION)
        policy_json = {
            "uid": str(uid),
            "description": "test",
            "subjects": [{"$.name": {"condition": "Equals",
                                     "value": "pyabac",
                                     "case_insensitive": False}}],
            "resources": [],
            "actions": [],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        }
        assert policy.to_json() == policy_json

    def test_from_json(self):
        uid = str(uuid.uuid4())
        policy = Policy(uid=uid,
                        description="test",
                        subjects=[{"$.name": Equals("pyabac")}],
                        resources=[],
                        actions=[],
                        context={},
                        effect=DENY_ACCESS,
                        collection=DEFAULT_POLICY_COLLECTION)
        policy_json = {
            "uid": uid,
            "description": "test",
            "subjects": [{"$.name": {"condition": "Equals",
                                     "value": "pyabac",
                                     "case_insensitive": False}}],
            "resources": [],
            "actions": [],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        }
        new_policy = Policy.from_json(policy_json)
        assert isinstance(new_policy, Policy)
        assert new_policy.to_json() == policy.to_json()

    @pytest.mark.parametrize("args", [
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": {"test": 1},
            "resources": [],
            "actions": [],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": {"test": 1},
            "actions": [],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": {"test": 1},
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": [],
            "context": 1.0,
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": [],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [1],
            "resources": [],
            "actions": [],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [1],
            "actions": [],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": [1],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "Attribute path not correct JsonPath",
            "subjects": [],
            "resources": [],
            "actions": [{")": Equals("1")}],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "Attribute value not of type condition",
            "subjects": [],
            "resources": [],
            "actions": [],
            "context": {"$": 1},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
    ])
    def test_create_policy_error(self, args):
        with pytest.raises(PolicyCreationError):
            Policy(**args)

    @pytest.mark.parametrize("args", [
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": {"test": 1},
            "resources": [],
            "actions": [],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": {"test": 1},
            "actions": [],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": {"test": 1},
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": [],
            "context": 1.0,
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": [],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [1],
            "resources": [],
            "actions": [],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [1],
            "actions": [],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "test",
            "subjects": [],
            "resources": [],
            "actions": [1],
            "context": {},
            "effect": "abc",
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "Attribute path not correct JsonPath",
            "subjects": [],
            "resources": [],
            "actions": [{")": Equals("1")}],
            "context": {},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
        {
            "uid": str(uuid.uuid4()),
            "description": "Attribute value not of type condition",
            "subjects": [],
            "resources": [],
            "actions": [],
            "context": {"$": 1},
            "effect": DENY_ACCESS,
            "collection": DEFAULT_POLICY_COLLECTION
        },
    ])
    def test_create_from_json_error(self, args):
        with pytest.raises(PolicyCreationError):
            Policy.from_json(args)

    def test_allow_access(self):
        policy = Policy(uid=uuid.uuid4(),
                        description="test",
                        subjects=[{"$.name": Equals("pyabac")}],
                        resources=[],
                        actions=[],
                        context={},
                        effect=DENY_ACCESS,
                        collection=DEFAULT_POLICY_COLLECTION)
        assert not policy.allow_access()
        policy.effect = ALLOW_ACCESS
        assert policy.allow_access()
