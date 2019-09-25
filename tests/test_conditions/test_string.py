"""
    String condition tests
"""

import pytest

from pyabac.exceptions import ConditionCreationError
from pyabac.conditions.string import Contains
from pyabac.conditions.string.ends_with import EndsWith
from pyabac.conditions.string import Equals
from pyabac.conditions.string import NotContains
from pyabac.conditions.string import NotEquals
from pyabac.conditions.string import RegexMatch
from pyabac.conditions.string.starts_with import StartsWith


class TestStringCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (Contains("2"), {"condition": "Contains", "value": "2", "case_insensitive": False}),
        (Contains("2", case_insensitive=True),
         {"condition": "Contains", "value": "2", "case_insensitive": True}),
        (NotContains("2"), {"condition": "NotContains", "value": "2", "case_insensitive": False}),
        (NotContains("2", case_insensitive=True),
         {"condition": "NotContains", "value": "2", "case_insensitive": True}),
        (Equals("2"), {"condition": "Equals", "value": "2", "case_insensitive": False}),
        (Equals("2", case_insensitive=True),
         {"condition": "Equals", "value": "2", "case_insensitive": True}),
        (NotEquals("2"), {"condition": "NotEquals", "value": "2", "case_insensitive": False}),
        (NotEquals("2", case_insensitive=True),
         {"condition": "NotEquals", "value": "2", "case_insensitive": True}),
        (StartsWith("2"), {"condition": "StartsWith", "value": "2", "case_insensitive": False}),
        (StartsWith("2", case_insensitive=True),
         {"condition": "StartsWith", "value": "2", "case_insensitive": True}),
        (EndsWith("2"), {"condition": "EndsWith", "value": "2", "case_insensitive": False}),
        (EndsWith("2", case_insensitive=True),
         {"condition": "EndsWith", "value": "2", "case_insensitive": True}),
        (RegexMatch("2"), {"condition": "RegexMatch", "value": "2"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (Contains("2"), {"condition": "Contains", "value": "2", "case_insensitive": False}),
        (Contains("2", case_insensitive=True),
         {"condition": "Contains", "value": "2", "case_insensitive": True}),
        (NotContains("2"), {"condition": "NotContains", "value": "2", "case_insensitive": False}),
        (NotContains("2", case_insensitive=True),
         {"condition": "NotContains", "value": "2", "case_insensitive": True}),
        (Equals("2"), {"condition": "Equals", "value": "2", "case_insensitive": False}),
        (Equals("2", case_insensitive=True),
         {"condition": "Equals", "value": "2", "case_insensitive": True}),
        (NotEquals("2"), {"condition": "NotEquals", "value": "2", "case_insensitive": False}),
        (NotEquals("2", case_insensitive=True),
         {"condition": "NotEquals", "value": "2", "case_insensitive": True}),
        (StartsWith("2"), {"condition": "StartsWith", "value": "2", "case_insensitive": False}),
        (StartsWith("2", case_insensitive=True),
         {"condition": "StartsWith", "value": "2", "case_insensitive": True}),
        (EndsWith("2"), {"condition": "EndsWith", "value": "2", "case_insensitive": False}),
        (EndsWith("2", case_insensitive=True),
         {"condition": "EndsWith", "value": "2", "case_insensitive": True}),
        (RegexMatch("2"), {"condition": "RegexMatch", "value": "2"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.from_json(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition, value, err_msg", [
        (Contains, 1, "Invalid argument type '{}' for string condition.".format(int)),
        (NotContains, [], "Invalid argument type '{}' for string condition.".format(list)),
        (Equals, {}, "Invalid argument type '{}' for string condition.".format(dict)),
        (NotEquals, None, "Invalid argument type '{}' for string condition.".format(type(None))),
        (StartsWith, {1, }, "Invalid argument type '{}' for string condition.".format(set)),
        (EndsWith, (), "Invalid argument type '{}' for string condition.".format(tuple)),
        (RegexMatch, "(", "Argument '{}' not a valid regexp string.".format("(")),
    ])
    def test_create_error(self, condition, value, err_msg):
        with pytest.raises(ConditionCreationError) as err:
            condition(value)
        assert str(err.value) == err_msg

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
    def test_create_from_json_error(self, condition_type, data):
        with pytest.raises(ConditionCreationError):
            condition_type.from_json(data)

    @pytest.mark.parametrize("condition, what, result", [
        (Contains("b"), "abc", True),
        (Contains("B"), "abc", False),
        (Contains("B", True), "abc", True),
        (Contains("b"), "cde", False),
        (Contains("b"), None, False),

        (NotContains("b"), "abc", False),
        (NotContains("b"), "cde", True),
        (NotContains("D"), "cde", True),
        (NotContains("D", True), "cde", False),
        (NotContains("D", True), None, False),

        (Equals("abc"), "abc", True),
        (Equals("ABC"), "abc", False),
        (Equals("ABC", True), "abc", True),
        (Equals("b"), "cde", False),
        (Equals("b"), None, False),

        (NotEquals("abc"), "abc", False),
        (NotEquals("ABC"), "abc", True),
        (NotEquals("ABC", True), "abc", False),
        (NotEquals("b"), "cde", True),
        (NotEquals("b"), None, False),

        (StartsWith("ab"), "abc", True),
        (StartsWith("AB"), "abc", False),
        (StartsWith("AB", True), "abc", True),
        (StartsWith("ab"), "ab", True),
        (StartsWith("ab"), "cab", False),
        (StartsWith("ab"), None, False),

        (EndsWith("ab"), "abc", False),
        (EndsWith("ab"), "ab", True),
        (EndsWith("ab"), "cab", True),
        (EndsWith("AB"), "cab", False),
        (EndsWith("AB", True), "cab", True),
        (EndsWith("AB", True), None, False),

        (RegexMatch(".*"), "foo", True),
        (RegexMatch("abc"), "abc", True),
        (RegexMatch("abc"), "abd", False),
        (RegexMatch(r"[\d\w]+"), "567asd", True),
        (RegexMatch(""), "", True),
        (RegexMatch(r"^python\?exe"), "python?exe", True),
        (RegexMatch(r"^python?exe"), "python?exe", False),
        (RegexMatch(r"^python?exe"), None, False),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
