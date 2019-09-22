"""
    Collection condition tests
"""

import pytest

from pyabac.exceptions import ConditionCreationError
from pyabac.policy.conditions.collection import AllInCondition
from pyabac.policy.conditions.collection import AllNotInCondition
from pyabac.policy.conditions.collection import AnyInCondition
from pyabac.policy.conditions.collection import AnyNotInCondition
from pyabac.policy.conditions.collection import IsEmptyCondition
from pyabac.policy.conditions.collection import IsInCondition
from pyabac.policy.conditions.collection import IsNotEmptyCondition
from pyabac.policy.conditions.collection import IsNotInCondition


class TestCollectionCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (AllInCondition([2]), {"condition": AllInCondition.name, "value": [2]}),
        (AllNotInCondition([{"test": 2}]), {"condition": AllNotInCondition.name, "value": [{"test": 2}]}),
        (AnyInCondition([2, {"test": 2}]), {"condition": AnyInCondition.name, "value": [2, {"test": 2}]}),
        (AnyNotInCondition([2, {"test": 2}, []]), {"condition": AnyNotInCondition.name, "value": [2, {"test": 2}, []]}),
        (IsInCondition([2]), {"condition": IsInCondition.name, "value": [2]}),
        (IsNotInCondition([2]), {"condition": IsNotInCondition.name, "value": [2]}),
        (IsEmptyCondition(), {"condition": IsEmptyCondition.name}),
        (IsNotEmptyCondition(), {"condition": IsNotEmptyCondition.name}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (AllInCondition([2]), {"condition": AllInCondition.name, "value": [2]}),
        (AllNotInCondition([{"test": 2}]), {"condition": AllNotInCondition.name, "value": [{"test": 2}]}),
        (AnyInCondition([2, {"test": 2}]), {"condition": AnyInCondition.name, "value": [2, {"test": 2}]}),
        (AnyNotInCondition([2, {"test": 2}, []]), {"condition": AnyNotInCondition.name, "value": [2, {"test": 2}, []]}),
        (IsInCondition([2]), {"condition": IsInCondition.name, "value": [2]}),
        (IsNotInCondition([2]), {"condition": IsNotInCondition.name, "value": [2]}),
        (IsEmptyCondition(), {"condition": IsEmptyCondition.name}),
        (IsNotEmptyCondition(), {"condition": IsNotEmptyCondition.name}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.from_json(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition, value, err_msg", [
        (AllInCondition, "test", "Invalid argument type '{}' for collection condition.".format(str)),
        (AllNotInCondition, 1, "Invalid argument type '{}' for collection condition.".format(int)),
        (AnyInCondition, 1.0, "Invalid argument type '{}' for collection condition.".format(float)),
        (AnyNotInCondition, {}, "Invalid argument type '{}' for collection condition.".format(dict)),
        (IsInCondition, None, "Invalid argument type '{}' for collection condition.".format(type(None))),
        (IsNotInCondition, object, "Invalid argument type '{}' for collection condition.".format(type(object))),
    ])
    def test_create_error(self, condition, value, err_msg):
        with pytest.raises(ConditionCreationError) as err:
            condition(value)
        assert str(err.value) == err_msg

    @pytest.mark.parametrize("condition_type, data", [
        (AllInCondition, {"condition": AllInCondition.name, "value": "test"}),
        (AllNotInCondition, {"condition": AllNotInCondition.name, "value": 1}),
        (AnyInCondition, {"condition": AnyInCondition.name, "value": {}}),
        (AnyNotInCondition, {"condition": AnyNotInCondition.name, "value": None}),
        (IsInCondition, {"condition": IsInCondition.name, "value": 1.0}),
        (IsNotInCondition, {"condition": IsNotInCondition.name, "value": object}),
        (IsEmptyCondition, {"condition": IsEmptyCondition.name, "value": []}),
        (IsNotEmptyCondition, {"condition": IsNotEmptyCondition.name, "value": 1}),
    ])
    def test_create_from_json_error(self, condition_type, data):
        with pytest.raises(ConditionCreationError):
            condition_type.from_json(data)

    @pytest.mark.parametrize("condition, what, result", [
        (AllInCondition([]), 1, False),
        (AllInCondition([]), [], True),
        (AllInCondition([2]), [], True),
        (AllInCondition([2]), [2], True),
        (AllInCondition([2]), [1, 2], False),
        (AllInCondition([3, 2]), [1, 2], False),
        (AllInCondition([1, 2, 3]), [1, 2], True),
        (AllInCondition([1, 2, 3]), None, False),

        (AllNotInCondition([]), 1, False),
        (AllNotInCondition([]), [], False),
        (AllNotInCondition([2]), [], False),
        (AllNotInCondition([2]), [2], False),
        (AllNotInCondition([2]), [1, 2], True),
        (AllNotInCondition([3, 2]), [1, 2], True),
        (AllNotInCondition([1, 2, 3]), [1, 2], False),
        (AllNotInCondition([1, 2, 3]), None, False),

        (AnyInCondition([]), 1, False),
        (AnyInCondition([]), [], False),
        (AnyInCondition([2]), [], False),
        (AnyInCondition([2]), [2], True),
        (AnyInCondition([2]), [1, 2], True),
        (AnyInCondition([3, 2]), [1, 4], False),
        (AnyInCondition([1, 2, 3]), [1, 2], True),
        (AnyInCondition([1, 2, 3]), None, False),

        (AnyNotInCondition([]), 1, False),
        (AnyNotInCondition([]), [], True),
        (AnyNotInCondition([2]), [], True),
        (AnyNotInCondition([2]), [2], False),
        (AnyNotInCondition([2]), [1, 2], False),
        (AnyNotInCondition([3, 2]), [1, 4], True),
        (AnyNotInCondition([1, 2, 3]), [1, 2], False),
        (AnyNotInCondition([1, 2, 3]), None, False),

        (IsInCondition([]), [], False),
        (IsInCondition([1, 2, 3]), 1, True),
        (IsInCondition([1, 2, 3]), 4, False),
        (IsInCondition([1, 2, 3]), None, False),

        (IsNotInCondition([]), [], True),
        (IsNotInCondition([1, 2, 3]), 1, False),
        (IsNotInCondition([1, 2, 3]), 4, True),
        (IsNotInCondition([1, 2, 3]), None, True),

        (IsEmptyCondition(), [], True),
        (IsEmptyCondition(), [1], False),
        (IsEmptyCondition(), None, False),

        (IsNotEmptyCondition(), [], False),
        (IsNotEmptyCondition(), [1], True),
        (IsNotEmptyCondition(), None, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
