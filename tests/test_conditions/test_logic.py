"""
    Logic condition tests
"""

import pytest

from pyabac.common.exceptions import ConditionCreationError
from pyabac.conditions.logic import And
from pyabac.conditions.logic import Not
from pyabac.conditions.logic import Or
from pyabac.conditions.numeric import Gt, Lt


class TestLogicCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (And(Gt(0.0), Lt(1.0)),
         {"condition": "And", "values": [
             {"condition": "Gt", "value": 0.0},
             {"condition": "Lt", "value": 1.0}
         ]}),

        (Or(Gt(0.0), Lt(1.0)),
         {"condition": "Or", "values": [
             {"condition": "Gt", "value": 0.0},
             {"condition": "Lt", "value": 1.0}
         ]}),

        (Not(Gt(1.0)),
         {"condition": "Not", "value": {
             "condition": "Gt", "value": 1.0
         }}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    def test_from_json_and(self):
        condition = And(Gt(0.0), Lt(1.0))
        condition_json = {
            "condition": "And", "values": [
                {"condition": "Gt", "value": 0.0},
                {"condition": "Lt", "value": 1.0}
            ]}
        new_condition = And.from_json(condition_json)
        assert isinstance(new_condition, And)
        assert len(condition.values) == len(new_condition.values)
        assert isinstance(new_condition.values[0], condition.values[0].__class__)
        assert new_condition.values[0].value == condition.values[0].value
        assert isinstance(new_condition.values[1], condition.values[1].__class__)
        assert new_condition.values[1].value == condition.values[1].value

    def test_from_json_or(self):
        condition = Or(Gt(0.0), Lt(1.0))
        condition_json = {
            "condition": "Or", "values": [
                {"condition": "Gt", "value": 0.0},
                {"condition": "Lt", "value": 1.0}
            ]}
        new_condition = Or.from_json(condition_json)
        assert isinstance(new_condition, Or)
        assert len(condition.values) == len(new_condition.values)
        assert isinstance(new_condition.values[0], condition.values[0].__class__)
        assert new_condition.values[0].value == condition.values[0].value
        assert isinstance(new_condition.values[1], condition.values[1].__class__)
        assert new_condition.values[1].value == condition.values[1].value

    def test_from_json_not(self):
        condition = Not(Gt(1.0))
        condition_json = {
            "condition": "Not", "value": {
                "condition": "Gt", "value": 1.0
            }}
        new_condition = Not.from_json(condition_json)
        assert isinstance(new_condition, Not)
        assert isinstance(new_condition.value, condition.value.__class__)
        assert new_condition.value.value == condition.value.value

    def test_create_error_and(self):
        with pytest.raises(ConditionCreationError) as err:
            And()
        assert str(err.value) == "No arguments provided in Logic condition."
        with pytest.raises(ConditionCreationError) as err:
            And(None)
        assert str(err.value) == "Invalid argument type '<class 'NoneType'>' for logic condition."

    def test_create_error_or(self):
        with pytest.raises(ConditionCreationError) as err:
            Or()
        assert str(err.value) == "No arguments provided in Logic condition."
        with pytest.raises(ConditionCreationError) as err:
            Or(1.0)
        assert str(err.value) == "Invalid argument type '<class 'float'>' for logic condition."

    def test_create_error_not(self):
        with pytest.raises(ConditionCreationError) as err:
            Not(1.0)
        assert str(err.value) == "Invalid argument type '<class 'float'>' for logic condition."

    @pytest.mark.parametrize("condition, what, result", [
        (And(Gt(0.0), Lt(1.0)), -1.5, False),
        (And(Gt(0.0), Lt(1.0)), 0.5, True),
        (And(Gt(0.0), Lt(1.0)), 1.5, False),

        (Or(Gt(1.0), Lt(0.0)), -1.5, True),
        (Or(Gt(1.0), Lt(0.0)), 0.5, False),
        (Or(Gt(1.0), Lt(0.0)), 1.5, True),

        (Not(Gt(1.0)), 0.5, True),
        (Not(Gt(1.0)), 1.5, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
