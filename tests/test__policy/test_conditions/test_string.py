"""
    String condition tests
"""

import pytest
from marshmallow import ValidationError

from py_abac.context import EvaluationContext
from py_abac._policy.conditions.schema import ConditionSchema
from py_abac._policy.conditions.string import Contains
from py_abac._policy.conditions.string import EndsWith
from py_abac._policy.conditions.string import Equals
from py_abac._policy.conditions.string import NotContains
from py_abac._policy.conditions.string import NotEquals
from py_abac._policy.conditions.string import RegexMatch
from py_abac._policy.conditions.string import StartsWith
from py_abac.request import AccessRequest


class TestStringCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (Contains(value="2"), {"condition": "Contains", "value": "2", "case_insensitive": False}),
        (Contains(value="2", case_insensitive=True),
         {"condition": "Contains", "value": "2", "case_insensitive": True}),
        (NotContains(value="2"), {"condition": "NotContains", "value": "2", "case_insensitive": False}),
        (NotContains(value="2", case_insensitive=True),
         {"condition": "NotContains", "value": "2", "case_insensitive": True}),
        (Equals(value="2"), {"condition": "Equals", "value": "2", "case_insensitive": False}),
        (Equals(value="2", case_insensitive=True),
         {"condition": "Equals", "value": "2", "case_insensitive": True}),
        (NotEquals(value="2"), {"condition": "NotEquals", "value": "2", "case_insensitive": False}),
        (NotEquals(value="2", case_insensitive=True),
         {"condition": "NotEquals", "value": "2", "case_insensitive": True}),
        (StartsWith(value="2"), {"condition": "StartsWith", "value": "2", "case_insensitive": False}),
        (StartsWith(value="2", case_insensitive=True),
         {"condition": "StartsWith", "value": "2", "case_insensitive": True}),
        (EndsWith(value="2"), {"condition": "EndsWith", "value": "2", "case_insensitive": False}),
        (EndsWith(value="2", case_insensitive=True),
         {"condition": "EndsWith", "value": "2", "case_insensitive": True}),
        (RegexMatch(value="2"), {"condition": "RegexMatch", "value": "2"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.dict() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (Contains(value="2"), {"condition": "Contains", "value": "2", "case_insensitive": False}),
        (Contains(value="2", case_insensitive=True),
         {"condition": "Contains", "value": "2", "case_insensitive": True}),
        (NotContains(value="2"), {"condition": "NotContains", "value": "2", "case_insensitive": False}),
        (NotContains(value="2", case_insensitive=True),
         {"condition": "NotContains", "value": "2", "case_insensitive": True}),
        (Equals(value="2"), {"condition": "Equals", "value": "2", "case_insensitive": False}),
        (Equals(value="2", case_insensitive=True),
         {"condition": "Equals", "value": "2", "case_insensitive": True}),
        (NotEquals(value="2"), {"condition": "NotEquals", "value": "2", "case_insensitive": False}),
        (NotEquals(value="2", case_insensitive=True),
         {"condition": "NotEquals", "value": "2", "case_insensitive": True}),
        (StartsWith(value="2"), {"condition": "StartsWith", "value": "2", "case_insensitive": False}),
        (StartsWith(value="2", case_insensitive=True),
         {"condition": "StartsWith", "value": "2", "case_insensitive": True}),
        (EndsWith(value="2"), {"condition": "EndsWith", "value": "2", "case_insensitive": False}),
        (EndsWith(value="2", case_insensitive=True),
         {"condition": "EndsWith", "value": "2", "case_insensitive": True}),
        (RegexMatch(value="2"), {"condition": "RegexMatch", "value": "2"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = ConditionSchema.parse_obj(condition_json)
        print(new_condition)
        assert new_condition.condition == condition.condition
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition_type, data", [
        (Contains, {"condition": "Contains", "value": 2, "case_insensitive": False}),
        (Contains, {"condition": "Contains", "value": "2", "case_insensitive": 2}),
        (NotContains, {"condition": "NotContains", "value": [], "case_insensitive": False}),
        (NotContains, {"condition": "NotContains", "value": "2", "case_insensitive": []}),
        (Equals, {"condition": "Equals", "value": {}, "case_insensitive": False}),
        (Equals, {"condition": "Equals", "value": "2", "case_insensitive": {}}),
        (NotEquals, {"condition": "NotEquals", "value": None, "case_insensitive": False}),
        (NotEquals, {"condition": "NotEquals", "value": "2", "case_insensitive": None}),
        (StartsWith, {"condition": "StartsWith", "value": {1, }, "case_insensitive": False}),
        (StartsWith, {"condition": "StartsWith", "value": "2", "case_insensitive": {1, }}),
        (EndsWith, {"condition": "EndsWith", "value": (), "case_insensitive": False}),
        (EndsWith, {"condition": "EndsWith", "value": "2", "case_insensitive": ()}),
        (RegexMatch, {"condition": "RegexMatch", "value": "("}),
    ])
    def test_create_error(self, condition_type, data):
        with pytest.raises(ValidationError):
            ConditionSchema().load(data)

    @pytest.mark.parametrize("condition, what, result", [
        (Contains(value="b"), "abc", True),
        (Contains(value="B"), "abc", False),
        (Contains(value="B", case_insensitive=True), "abc", True),
        (Contains(value="b"), "cde", False),
        (Contains(value="b"), None, False),

        (NotContains(value="b"), "abc", False),
        (NotContains(value="b"), "cde", True),
        (NotContains(value="D"), "cde", True),
        (NotContains(value="D", case_insensitive=True), "cde", False),
        (NotContains(value="D", case_insensitive=True), None, False),

        (Equals(value="abc"), "abc", True),
        (Equals(value="ABC"), "abc", False),
        (Equals(value="ABC", case_insensitive=True), "abc", True),
        (Equals(value="b"), "cde", False),
        (Equals(value="b"), None, False),

        (NotEquals(value="abc"), "abc", False),
        (NotEquals(value="ABC"), "abc", True),
        (NotEquals(value="ABC", case_insensitive=True), "abc", False),
        (NotEquals(value="b"), "cde", True),
        (NotEquals(value="b"), None, False),

        (StartsWith(value="ab"), "abc", True),
        (StartsWith(value="AB"), "abc", False),
        (StartsWith(value="AB", case_insensitive=True), "abc", True),
        (StartsWith(value="ab"), "ab", True),
        (StartsWith(value="ab"), "cab", False),
        (StartsWith(value="ab"), None, False),

        (EndsWith(value="ab"), "abc", False),
        (EndsWith(value="ab"), "ab", True),
        (EndsWith(value="ab"), "cab", True),
        (EndsWith(value="AB"), "cab", False),
        (EndsWith(value="AB", case_insensitive=True), "cab", True),
        (EndsWith(value="AB", case_insensitive=True), None, False),

        (RegexMatch(value=".*"), "foo", True),
        (RegexMatch(value="abc"), "abc", True),
        (RegexMatch(value="abc"), "abd", False),
        (RegexMatch(value=r"[\d\w]+"), "567asd", True),
        (RegexMatch(value=""), "", True),
        (RegexMatch(value=r"^python\?exe"), "python?exe", True),
        (RegexMatch(value=r"^python?exe"), "python?exe", False),
        (RegexMatch(value=r"^python?exe"), None, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        request = AccessRequest(subject={"attributes": {"what": what}}, resource={}, action={}, context={})
        ctx = EvaluationContext(request)
        ctx.ace = "subject"
        ctx.attribute_path = "$.what"
        assert condition.is_satisfied(ctx) == result
