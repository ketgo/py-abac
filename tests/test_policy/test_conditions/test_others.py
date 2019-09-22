"""
    Other conditions tests
"""

import pytest

from pyabac.exceptions import ConditionCreationError
from pyabac.policy.conditions.exists import ExistsCondition
from pyabac.policy.conditions.exists import NotExistsCondition
from pyabac.policy.conditions.net import CIDRCondition


class TestLogicCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDRCondition("127.0.0.0/16"), {"condition": CIDRCondition.name, "value": "127.0.0.0/16"}),
        (ExistsCondition(), {"condition": ExistsCondition.name}),
        (NotExistsCondition(), {"condition": NotExistsCondition.name}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDRCondition("127.0.0.0/16"), {"condition": CIDRCondition.name, "value": "127.0.0.0/16"}),
        (ExistsCondition(), {"condition": ExistsCondition.name}),
        (NotExistsCondition(), {"condition": NotExistsCondition.name}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.from_json(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition, value, err_msg", [
        (CIDRCondition, 1.0, "Invalid argument type '{}' for network condition.".format(type(1.0))),
    ])
    def test_create_error(self, condition, value, err_msg):
        with pytest.raises(ConditionCreationError) as err:
            condition(value)
        assert str(err.value) == err_msg

    @pytest.mark.parametrize("condition_type, data", [
        (CIDRCondition, {"condition": CIDRCondition.name, "value": 1.0}),
    ])
    def test_create_from_json_error(self, condition_type, data):
        with pytest.raises(ConditionCreationError):
            condition_type.from_json(data)

    @pytest.mark.parametrize("condition, what, result", [
        (CIDRCondition("127.0.0.0/24"), "10.0.0.0", False),
        (CIDRCondition("127.0.0.0/24"), "127.0.0.1", True),

        (ExistsCondition(), None, False),
        (ExistsCondition(), 1.0, True),

        (NotExistsCondition(), None, True),
        (NotExistsCondition(), 1.0, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
