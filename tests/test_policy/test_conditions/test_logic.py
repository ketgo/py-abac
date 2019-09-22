"""
    Logic condition tests
"""

import pytest

from pyabac.exceptions import ConditionCreationError
from pyabac.policy.conditions.logic import AndCondition
from pyabac.policy.conditions.logic import NotCondition
from pyabac.policy.conditions.logic import OrCondition
from pyabac.policy.conditions.numeric import GreaterCondition, LessCondition


class TestLogicCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (AndCondition(GreaterCondition(0.0), LessCondition(1.0)),
         {"condition": AndCondition.name, "values": [
             {"condition": GreaterCondition.name, "value": 0.0},
             {"condition": LessCondition.name, "value": 1.0}
         ]}),

        (OrCondition(GreaterCondition(0.0), LessCondition(1.0)),
         {"condition": OrCondition.name, "values": [
             {"condition": GreaterCondition.name, "value": 0.0},
             {"condition": LessCondition.name, "value": 1.0}
         ]}),

        (NotCondition(GreaterCondition(1.0)),
         {"condition": NotCondition.name, "value": {
             "condition": GreaterCondition.name, "value": 1.0
         }}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    def test_from_json_and(self):
        condition = AndCondition(GreaterCondition(0.0), LessCondition(1.0))
        condition_json = {
            "condition": AndCondition.name, "values": [
                {"condition": GreaterCondition.name, "value": 0.0},
                {"condition": LessCondition.name, "value": 1.0}
            ]}
        new_condition = AndCondition.from_json(condition_json)
        assert isinstance(new_condition, AndCondition)
        assert len(condition.values) == len(new_condition.values)
        assert isinstance(new_condition.values[0], condition.values[0].__class__)
        assert new_condition.values[0].value == condition.values[0].value
        assert isinstance(new_condition.values[1], condition.values[1].__class__)
        assert new_condition.values[1].value == condition.values[1].value

    def test_from_json_or(self):
        condition = OrCondition(GreaterCondition(0.0), LessCondition(1.0))
        condition_json = {
            "condition": OrCondition.name, "values": [
                {"condition": GreaterCondition.name, "value": 0.0},
                {"condition": LessCondition.name, "value": 1.0}
            ]}
        new_condition = OrCondition.from_json(condition_json)
        assert isinstance(new_condition, OrCondition)
        assert len(condition.values) == len(new_condition.values)
        assert isinstance(new_condition.values[0], condition.values[0].__class__)
        assert new_condition.values[0].value == condition.values[0].value
        assert isinstance(new_condition.values[1], condition.values[1].__class__)
        assert new_condition.values[1].value == condition.values[1].value

    def test_from_json_not(self):
        condition = NotCondition(GreaterCondition(1.0))
        condition_json = {
            "condition": NotCondition.name, "value": {
                "condition": GreaterCondition.name, "value": 1.0
            }}
        new_condition = NotCondition.from_json(condition_json)
        assert isinstance(new_condition, NotCondition)
        assert isinstance(new_condition.value, condition.value.__class__)
        assert new_condition.value.value == condition.value.value

    def test_create_error_and(self):
        with pytest.raises(ConditionCreationError) as err:
            AndCondition()
        assert str(err.value) == "No arguments provided in Logic condition."
        with pytest.raises(ConditionCreationError) as err:
            AndCondition(None)
        assert str(err.value) == "Invalid argument type '<class 'NoneType'>' for logic condition."

    def test_create_error_or(self):
        with pytest.raises(ConditionCreationError) as err:
            OrCondition()
        assert str(err.value) == "No arguments provided in Logic condition."
        with pytest.raises(ConditionCreationError) as err:
            OrCondition(1.0)
        assert str(err.value) == "Invalid argument type '<class 'float'>' for logic condition."

    def test_create_error_not(self):
        with pytest.raises(ConditionCreationError) as err:
            NotCondition(1.0)
        assert str(err.value) == "Invalid argument type '<class 'float'>' for logic condition."

    @pytest.mark.parametrize("condition, what, result", [
        (AndCondition(GreaterCondition(0.0), LessCondition(1.0)), -1.5, False),
        (AndCondition(GreaterCondition(0.0), LessCondition(1.0)), 0.5, True),
        (AndCondition(GreaterCondition(0.0), LessCondition(1.0)), 1.5, False),

        (OrCondition(GreaterCondition(1.0), LessCondition(0.0)), -1.5, True),
        (OrCondition(GreaterCondition(1.0), LessCondition(0.0)), 0.5, False),
        (OrCondition(GreaterCondition(1.0), LessCondition(0.0)), 1.5, True),

        (NotCondition(GreaterCondition(1.0)), 0.5, True),
        (NotCondition(GreaterCondition(1.0)), 1.5, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
