"""
    Other conditions tests
"""

import pytest

from pyabac.common.exceptions import ConditionCreationError
from pyabac.conditions.others import Any
from pyabac.conditions.others import CIDR
from pyabac.conditions.others import Exists
from pyabac.conditions.others import NotExists


class TestOtherCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDR("127.0.0.0/16"), {"condition": "CIDR", "value": "127.0.0.0/16"}),
        (Exists(), {"condition": "Exists"}),
        (NotExists(), {"condition": "NotExists"}),
        (Any(), {"condition": "Any"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (CIDR("127.0.0.0/16"), {"condition": "CIDR", "value": "127.0.0.0/16"}),
        (Exists(), {"condition": "Exists"}),
        (NotExists(), {"condition": "NotExists"}),
        (Any(), {"condition": "Any"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.from_json(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition, value, err_msg", [
        (CIDR, 1.0, "Invalid argument type '{}' for network condition.".format(type(1.0))),
    ])
    def test_create_error(self, condition, value, err_msg):
        with pytest.raises(ConditionCreationError) as err:
            condition(value)
        assert str(err.value) == err_msg

    @pytest.mark.parametrize("condition_type, data", [
        (CIDR, {"condition": "CIDR", "value": 1.0}),
    ])
    def test_create_from_json_error(self, condition_type, data):
        with pytest.raises(ConditionCreationError):
            condition_type.from_json(data)

    @pytest.mark.parametrize("condition, what, result", [
        (CIDR("127.0.0.0/24"), "10.0.0.0", False),
        (CIDR("127.0.0.0/24"), "127.0.0.1", True),
        (CIDR("127.0.0.0/24"), ")", False),
        (CIDR("127.0.0.0/24"), None, False),

        (Exists(), None, False),
        (Exists(), 1.0, True),

        (NotExists(), None, True),
        (NotExists(), 1.0, False),

        (Any(), None, True),
        (Any(), 1.0, True),
        (Any(), {"value": 1.0}, True),
        (Any(), [1.0, 2.0, "a"], True),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
