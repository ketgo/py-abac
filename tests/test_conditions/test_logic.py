"""
    Logic condition tests
"""

import pytest
from marshmallow import ValidationError

from pyabac.conditions.logic import AllOf
from pyabac.conditions.logic import AnyOf
from pyabac.conditions.logic import Not
from pyabac.conditions.numeric import Gt, Lt
from pyabac.conditions.schema import ConditionSchema
from pyabac.context import EvaluationContext
from pyabac.request import Request


class TestLogicCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (AllOf([Gt(0.0), Lt(1.0)]),
         {"condition": "AllOf", "values": [
             {"condition": "Gt", "value": 0.0},
             {"condition": "Lt", "value": 1.0}
         ]}),

        (AnyOf([Gt(0.0), Lt(1.0)]),
         {"condition": "AnyOf", "values": [
             {"condition": "Gt", "value": 0.0},
             {"condition": "Lt", "value": 1.0}
         ]}),

        (Not(Gt(1.0)),
         {"condition": "Not", "value": {
             "condition": "Gt", "value": 1.0
         }}),
    ])
    def test_to_json(self, condition, condition_json):
        assert ConditionSchema().dump(condition) == condition_json

    def test_from_json_and(self):
        condition = AllOf([Gt(0.0), Lt(1.0)])
        condition_json = {
            "condition": "AllOf", "values": [
                {"condition": "Gt", "value": 0.0},
                {"condition": "Lt", "value": 1.0}
            ]}
        new_condition = ConditionSchema().load(condition_json)
        assert isinstance(new_condition, AllOf)
        assert len(condition.values) == len(new_condition.values)
        assert isinstance(new_condition.values[0], condition.values[0].__class__)
        assert new_condition.values[0].value == condition.values[0].value
        assert isinstance(new_condition.values[1], condition.values[1].__class__)
        assert new_condition.values[1].value == condition.values[1].value

    def test_from_json_or(self):
        condition = AnyOf([Gt(0.0), Lt(1.0)])
        condition_json = {
            "condition": "AnyOf", "values": [
                {"condition": "Gt", "value": 0.0},
                {"condition": "Lt", "value": 1.0}
            ]}
        new_condition = ConditionSchema().load(condition_json)
        assert isinstance(new_condition, AnyOf)
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
        new_condition = ConditionSchema().load(condition_json)
        assert isinstance(new_condition, Not)
        assert isinstance(new_condition.value, condition.value.__class__)
        assert new_condition.value.value == condition.value.value

    @pytest.mark.parametrize("condition_json", [
        {"condition": "AllOf", "values": []},
        {"condition": "AllOf", "values": None},
        {"condition": "AllOf", "values": [None]},
        {"condition": "AnyOf", "values": []},
        {"condition": "AnyOf", "values": None},
        {"condition": "AnyOf", "values": [None]},
        {"condition": "Not", "values": 1.0},
    ])
    def test_create_error(self, condition_json):
        with pytest.raises(ValidationError):
            ConditionSchema().load(condition_json)

    @pytest.mark.parametrize("condition, what, result", [
        (AllOf([Gt(0.0), Lt(1.0)]), -1.5, False),
        (AllOf([Gt(0.0), Lt(1.0)]), 0.5, True),
        (AllOf([Gt(0.0), Lt(1.0)]), 1.5, False),

        (AnyOf([Gt(1.0), Lt(0.0)]), -1.5, True),
        (AnyOf([Gt(1.0), Lt(0.0)]), 0.5, False),
        (AnyOf([Gt(1.0), Lt(0.0)]), 1.5, True),

        (Not(Gt(1.0)), 0.5, True),
        (Not(Gt(1.0)), 1.5, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = Request(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
