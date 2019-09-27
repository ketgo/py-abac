"""
    Numeric condition tests
"""

import pytest

from pyabac.exceptions import ConditionCreationError
from pyabac.policy.conditions.numeric import Eq
from pyabac.policy.conditions.numeric import Gt
from pyabac.policy.conditions.numeric import Gte
from pyabac.policy.conditions.numeric import Lt
from pyabac.policy.conditions.numeric import Lte
from pyabac.policy.conditions.numeric import Neq


class TestNumericCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (Eq(2), {"condition": "Eq", "value": 2}),
        (Eq(3.0), {"condition": "Eq", "value": 3.0}),
        (Gt(2), {"condition": "Gt", "value": 2}),
        (Gt(3.0), {"condition": "Gt", "value": 3.0}),
        (Lt(2), {"condition": "Lt", "value": 2}),
        (Lt(3.0), {"condition": "Lt", "value": 3.0}),
        (Gte(2), {"condition": "Gte", "value": 2}),
        (Gte(3.0), {"condition": "Gte", "value": 3.0}),
        (Lte(2), {"condition": "Lte", "value": 2}),
        (Lte(3.0), {"condition": "Lte", "value": 3.0}),
        (Neq(2), {"condition": "Neq", "value": 2}),
        (Neq(3.0), {"condition": "Neq", "value": 3.0}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    @pytest.mark.parametrize("condition_type, value, condition_json", [
        (Eq, 2, {"condition": "Eq", "value": 2}),
        (Eq, 3.0, {"condition": "Eq", "value": 3.0}),
        (Gt, 2, {"condition": "Gt", "value": 2}),
        (Gt, 3.0, {"condition": "Gt", "value": 3.0}),
        (Lt, 2, {"condition": "Lt", "value": 2}),
        (Lt, 3.0, {"condition": "Lt", "value": 3.0}),
        (Gte, 2, {"condition": "Gte", "value": 2}),
        (Gte, 3.0, {"condition": "Gte", "value": 3.0}),
        (Lte, 2, {"condition": "Lte", "value": 2}),
        (Lte, 3.0, {"condition": "Lte", "value": 3.0}),
        (Neq, 2, {"condition": "Neq", "value": 2}),
        (Neq, 3.0, {"condition": "Neq", "value": 3.0}),
    ])
    def test_from_json(self, condition_type, value, condition_json):
        condition = condition_type.from_json(condition_json)
        assert isinstance(condition, condition_type)
        assert condition.value == value

    @pytest.mark.parametrize("condition, value, err_msg", [
        (Eq, "test", "Invalid argument type '{}' for numeric condition.".format(str)),
        (Gt, [], "Invalid argument type '{}' for numeric condition.".format(list)),
        (Lt, {}, "Invalid argument type '{}' for numeric condition.".format(dict)),
        (Gte, None, "Invalid argument type '{}' for numeric condition.".format(type(None))),
        (Lte, {1, }, "Invalid argument type '{}' for numeric condition.".format(set)),
        (Neq, (), "Invalid argument type '{}' for numeric condition.".format(tuple)),
    ])
    def test_create_error(self, condition, value, err_msg):
        with pytest.raises(ConditionCreationError) as err:
            condition(value)
        assert str(err.value) == err_msg

    @pytest.mark.parametrize("condition_type, data", [
        (Eq, {"condition": "Eq", "value": "test"}),
        (Gt, {"condition": "Gt", "value": []}),
        (Lt, {"condition": "Lt", "value": {}}),
        (Gte, {"condition": "Gte", "value": None}),
        (Lte, {"condition": "Lte", "value": {1, }}),
        (Neq, {"condition": "Neq", "value": ()}),
    ])
    def test_create_from_json_error(self, condition_type, data):
        with pytest.raises(ConditionCreationError):
            condition_type.from_json(data)

    @pytest.mark.parametrize("condition, what, result", [
        (Eq(2), 2, True),
        (Eq(2), 2.0, True),
        (Eq(2.0), 2, True),
        (Eq(2.0), 2.0, True),
        (Eq(2), 3.0, False),
        (Eq(2), None, False),

        (Gt(2), 2, False),
        (Gt(2), 2.1, True),
        (Gt(2), 1.9, False),
        (Gt(2), None, False),

        (Gte(2), 2, True),
        (Gte(2), 2.1, True),
        (Gte(2), 1.9, False),
        (Gte(2), None, False),

        (Lt(2), 2, False),
        (Lt(2), 2.1, False),
        (Lt(2), 1.9, True),
        (Lt(2), None, False),

        (Lte(2), 2, True),
        (Lte(2), 2.1, False),
        (Lte(2), 1.9, True),
        (Lte(2), None, False),

        (Neq(2), 2, False),
        (Neq(2.0), 2, False),
        (Neq(2), 2.0, False),
        (Neq(2), 1.9, True),
        (Neq(2), None, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
