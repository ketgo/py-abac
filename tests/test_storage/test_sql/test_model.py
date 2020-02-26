from typing import List

from py_abac.policy import Policy
from py_abac.storage.sql.model import PolicyModel, TargetModel


def policy_model_assert(policy_model: PolicyModel, policy: Policy):
    """
        Assert if the given policy model object `policy_model` is equal to the policy object `policy`
    """

    def assert_targets(target_models: List[TargetModel], target_ids):
        _target_ids = target_ids if isinstance(target_ids, list) else [target_ids]
        assert len(target_models) == len(_target_ids)
        for x in range(len(_target_ids)):
            assert target_models[x].target_id.replace('%', '*') == _target_ids[x]

    assert policy_model.uid == policy.uid
    assert policy_model.json == policy.to_json()
    assert_targets(policy_model.actions, policy.targets.action_id)
    assert_targets(policy_model.subjects, policy.targets.subject_id)
    assert_targets(policy_model.resources, policy.targets.resource_id)


class TestModel:
    POLICY_JSON = {
        "uid": "1",
        "description": "Max is not allowed to print any resource",
        "effect": "deny",
        "rules": {
            "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
            "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
            "action": {"$.method": {"condition": "Equals", "value": "print"}},
            "context": {}
        },
        "targets": {"subject_id": "user:1"},
        "priority": 0
    }

    def test_from_policy(self):
        policy = Policy.from_json(self.POLICY_JSON)
        p_model = PolicyModel.from_policy(policy)
        policy_model_assert(p_model, policy)

    def test_update(self):
        policy = Policy.from_json(self.POLICY_JSON)
        p_model = PolicyModel.from_policy(policy)

        new_policy_json = self.POLICY_JSON.copy()
        new_policy_json["priority"] = 1
        new_policy = Policy.from_json(new_policy_json)
        p_model.update(new_policy)
        policy_model_assert(p_model, new_policy)

    def test_to_policy(self):
        policy = Policy.from_json(self.POLICY_JSON)
        p_model = PolicyModel.from_policy(policy)
        _policy = p_model.to_policy()
        assert policy.to_json() == _policy.to_json()

    def test_get_filter(self):
        policy = Policy.from_json(self.POLICY_JSON)
        p_model = PolicyModel.from_policy(policy)
        _filter = p_model.get_filter("1", "1", "1")
        assert len(_filter) == 3
