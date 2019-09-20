"""
    Numeric condition tests
"""

import pytest

from pyabac.policy.conditions.numeric import EqualCondition
from pyabac.policy.conditions.numeric import GreaterCondition
from pyabac.policy.conditions.numeric import GreaterEqualCondition
from pyabac.policy.conditions.numeric import LessCondition
from pyabac.policy.conditions.numeric import LessEqualCondition


class TestNumericCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (EqualCondition(2), {"condition": EqualCondition.name, "value": 2}),
        (EqualCondition(3.0), {"condition": EqualCondition.name, "value": 3.0}),
        (GreaterCondition(2), {"condition": GreaterCondition.name, "value": 2}),
        (GreaterCondition(3.0), {"condition": GreaterCondition.name, "value": 3.0}),
        (LessCondition(2), {"condition": LessCondition.name, "value": 2}),
        (LessCondition(3.0), {"condition": LessCondition.name, "value": 3.0}),
        (GreaterEqualCondition(2), {"condition": GreaterEqualCondition.name, "value": 2}),
        (GreaterEqualCondition(3.0), {"condition": GreaterEqualCondition.name, "value": 3.0}),
        (LessEqualCondition(2), {"condition": LessEqualCondition.name, "value": 2}),
        (LessEqualCondition(3.0), {"condition": LessEqualCondition.name, "value": 3.0}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    @pytest.mark.parametrize("condition_type, value, condition_json", [
        (EqualCondition, 2, {"condition": EqualCondition.name, "value": 2}),
        (EqualCondition, 3.0, {"condition": EqualCondition.name, "value": 3.0}),
        (GreaterCondition, 2, {"condition": GreaterCondition.name, "value": 2}),
        (GreaterCondition, 3.0, {"condition": GreaterCondition.name, "value": 3.0}),
        (LessCondition, 2, {"condition": LessCondition.name, "value": 2}),
        (LessCondition, 3.0, {"condition": LessCondition.name, "value": 3.0}),
        (GreaterEqualCondition, 2, {"condition": GreaterEqualCondition.name, "value": 2}),
        (GreaterEqualCondition, 3.0, {"condition": GreaterEqualCondition.name, "value": 3.0}),
        (LessEqualCondition, 2, {"condition": LessEqualCondition.name, "value": 2}),
        (LessEqualCondition, 3.0, {"condition": LessEqualCondition.name, "value": 3.0}),
    ])
    def test_from_json(self, condition_type, value, condition_json):
        condition = condition_type.from_json(condition_json)
        assert isinstance(condition, condition_type)
        assert condition.value == value

    @pytest.mark.parametrize("condition, value, err_msg", [
        (EqualCondition, "test", "Invalid argument type '{}' for numeric condition.".format(str)),
        (GreaterCondition, [], "Invalid argument type '{}' for numeric condition.".format(list)),
        (LessCondition, {}, "Invalid argument type '{}' for numeric condition.".format(dict)),
        (GreaterEqualCondition, None, "Invalid argument type '{}' for numeric condition.".format(type(None))),
        (LessEqualCondition, {1, }, "Invalid argument type '{}' for numeric condition.".format(set)),
        (LessEqualCondition, (), "Invalid argument type '{}' for numeric condition.".format(tuple)),
    ])
    def test_type_error(self, condition, value, err_msg):
        with pytest.raises(TypeError) as err:
            condition(value)
        assert str(err.value) == err_msg

    @pytest.mark.parametrize("condition, what, result", [
        (EqualCondition(2), 2, True),
        (EqualCondition(2), 2.0, True),
        (EqualCondition(2.0), 2, True),
        (EqualCondition(2.0), 2.0, True),
        (EqualCondition(2), 3.0, False),
        (GreaterCondition(2), 2, False),
        (GreaterCondition(2), 2.1, True),
        (GreaterCondition(2), 1.9, False),
        (GreaterEqualCondition(2), 2, True),
        (GreaterEqualCondition(2), 2.1, True),
        (GreaterEqualCondition(2), 1.9, False),
        (LessCondition(2), 2, False),
        (LessCondition(2), 2.1, False),
        (LessCondition(2), 1.9, True),
        (LessEqualCondition(2), 2, True),
        (LessEqualCondition(2), 2.1, False),
        (LessEqualCondition(2), 1.9, True),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
