"""
    Logic condition tests
"""

import pytest
from pydantic import ValidationError

from py_abac._policy.conditions.logic import AllOf
from py_abac._policy.conditions.logic import AnyOf
from py_abac._policy.conditions.logic import Not
from py_abac._policy.conditions.numeric import Gt, Lt
from py_abac.context import EvaluationContext
from py_abac.request import AccessRequest


class TestLogicCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (AllOf(values=[Gt(value=0.0), Lt(value=1.0)]),
         {"condition": "AllOf", "values": [
             {"condition": "Gt", "value": 0.0},
             {"condition": "Lt", "value": 1.0}
         ]}),

        (AnyOf(values=[Gt(value=0.0), Lt(value=1.0)]),
         {"condition": "AnyOf", "values": [
             {"condition": "Gt", "value": 0.0},
             {"condition": "Lt", "value": 1.0}
         ]}),

        (Not(value=Gt(value=1.0)),
         {"condition": "Not", "value": {
             "condition": "Gt", "value": 1.0
         }}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.dict() == condition_json

    def test_from_json_and(self):
        condition = AllOf(values=[Gt(value=0.0), Lt(value=1.0)])
        condition_json = {
            "condition": "AllOf", "values": [
                {"condition": "Gt", "value": 0.0},
                {"condition": "Lt", "value": 1.0}
            ]}
        new_condition = AllOf.parse_obj(condition_json)
        assert isinstance(new_condition, AllOf)
        assert len(condition.values) == len(new_condition.values)
        assert isinstance(new_condition.values[0], condition.values[0].__class__)
        assert new_condition.values[0].value == condition.values[0].value
        assert isinstance(new_condition.values[1], condition.values[1].__class__)
        assert new_condition.values[1].value == condition.values[1].value

    def test_from_json_or(self):
        condition = AnyOf(values=[Gt(value=0.0), Lt(value=1.0)])
        condition_json = {
            "condition": "AnyOf", "values": [
                {"condition": "Gt", "value": 0.0},
                {"condition": "Lt", "value": 1.0}
            ]}
        new_condition = AnyOf.parse_obj(condition_json)
        assert isinstance(new_condition, AnyOf)
        assert len(condition.values) == len(new_condition.values)
        assert isinstance(new_condition.values[0], condition.values[0].__class__)
        assert new_condition.values[0].value == condition.values[0].value
        assert isinstance(new_condition.values[1], condition.values[1].__class__)
        assert new_condition.values[1].value == condition.values[1].value

    def test_from_json_not(self):
        condition = Not(value=Gt(value=1.0))
        condition_json = {
            "condition": "Not", "value": {
                "condition": "Gt", "value": 1.0
            }}
        new_condition = Not.parse_obj(condition_json)
        assert isinstance(new_condition, Not)
        assert isinstance(new_condition.value, condition.value.__class__)
        assert new_condition.value.value == condition.value.value

    @pytest.mark.parametrize("condition_type, condition_json", [
        (AllOf, {"condition": "AllOf", "values": []}),
        (AllOf, {"condition": "AllOf", "values": None}),
        (AllOf, {"condition": "AllOf", "values": [None]}),
        (AnyOf, {"condition": "AnyOf", "values": []}),
        (AnyOf, {"condition": "AnyOf", "values": None}),
        (AnyOf, {"condition": "AnyOf", "values": [None]}),
        (Not, {"condition": "Not", "values": 1.0}),
    ])
    def test_create_error(self, condition_type, condition_json):
        with pytest.raises(ValidationError):
            condition_type.parse_obj(condition_json)

    @pytest.mark.parametrize("condition, what, result", [
        (AllOf(values=[Gt(value=0.0), Lt(value=1.0)]), -1.5, False),
        (AllOf(values=[Gt(value=0.0), Lt(value=1.0)]), 0.5, True),
        (AllOf(values=[Gt(value=0.0), Lt(value=1.0)]), 1.5, False),

        (AnyOf(values=[Gt(value=1.0), Lt(value=0.0)]), -1.5, True),
        (AnyOf(values=[Gt(value=1.0), Lt(value=0.0)]), 0.5, False),
        (AnyOf(values=[Gt(value=1.0), Lt(value=0.0)]), 1.5, True),

        (Not(value=Gt(value=1.0)), 0.5, True),
        (Not(value=Gt(value=1.0)), 1.5, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
