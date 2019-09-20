"""
    String condition tests
"""

import pytest

from pyabac.policy.conditions.string.contains import ContainsCondition
from pyabac.policy.conditions.string.not_contains import NotContainsCondition
from pyabac.policy.conditions.string.equals import EqualsCondition
from pyabac.policy.conditions.string.not_equals import NotEqualsCondition
from pyabac.policy.conditions.string.starts_with import StartsWithCondition
from pyabac.policy.conditions.string.ends_with import EndsWithCondition
from pyabac.policy.conditions.string.regex_match import RegexMatchCondition


class TestStringCondition(object):

    @pytest.mark.parametrize("condition, condition_json", [
        (ContainsCondition("2"), {"condition": ContainsCondition.name, "value": "2", "case_insensitive": False}),
        (ContainsCondition("2", case_insensitive=True),
         {"condition": ContainsCondition.name, "value": "2", "case_insensitive": True}),
        (NotContainsCondition("2"), {"condition": NotContainsCondition.name, "value": "2", "case_insensitive": False}),
        (NotContainsCondition("2", case_insensitive=True),
         {"condition": NotContainsCondition.name, "value": "2", "case_insensitive": True}),
        (EqualsCondition("2"), {"condition": EqualsCondition.name, "value": "2", "case_insensitive": False}),
        (EqualsCondition("2", case_insensitive=True),
         {"condition": EqualsCondition.name, "value": "2", "case_insensitive": True}),
        (NotEqualsCondition("2"), {"condition": NotEqualsCondition.name, "value": "2", "case_insensitive": False}),
        (NotEqualsCondition("2", case_insensitive=True),
         {"condition": NotEqualsCondition.name, "value": "2", "case_insensitive": True}),
        (StartsWithCondition("2"), {"condition": StartsWithCondition.name, "value": "2", "case_insensitive": False}),
        (StartsWithCondition("2", case_insensitive=True),
         {"condition": StartsWithCondition.name, "value": "2", "case_insensitive": True}),
        (EndsWithCondition("2"), {"condition": EndsWithCondition.name, "value": "2", "case_insensitive": False}),
        (EndsWithCondition("2", case_insensitive=True),
         {"condition": EndsWithCondition.name, "value": "2", "case_insensitive": True}),
        (RegexMatchCondition("2"), {"condition": RegexMatchCondition.name, "value": "2"}),
    ])
    def test_to_json(self, condition, condition_json):
        assert condition.to_json() == condition_json

    @pytest.mark.parametrize("condition, condition_json", [
        (ContainsCondition("2"), {"condition": ContainsCondition.name, "value": "2", "case_insensitive": False}),
        (ContainsCondition("2", case_insensitive=True),
         {"condition": ContainsCondition.name, "value": "2", "case_insensitive": True}),
        (NotContainsCondition("2"), {"condition": NotContainsCondition.name, "value": "2", "case_insensitive": False}),
        (NotContainsCondition("2", case_insensitive=True),
         {"condition": NotContainsCondition.name, "value": "2", "case_insensitive": True}),
        (EqualsCondition("2"), {"condition": EqualsCondition.name, "value": "2", "case_insensitive": False}),
        (EqualsCondition("2", case_insensitive=True),
         {"condition": EqualsCondition.name, "value": "2", "case_insensitive": True}),
        (NotEqualsCondition("2"), {"condition": NotEqualsCondition.name, "value": "2", "case_insensitive": False}),
        (NotEqualsCondition("2", case_insensitive=True),
         {"condition": NotEqualsCondition.name, "value": "2", "case_insensitive": True}),
        (StartsWithCondition("2"), {"condition": StartsWithCondition.name, "value": "2", "case_insensitive": False}),
        (StartsWithCondition("2", case_insensitive=True),
         {"condition": StartsWithCondition.name, "value": "2", "case_insensitive": True}),
        (EndsWithCondition("2"), {"condition": EndsWithCondition.name, "value": "2", "case_insensitive": False}),
        (EndsWithCondition("2", case_insensitive=True),
         {"condition": EndsWithCondition.name, "value": "2", "case_insensitive": True}),
        (RegexMatchCondition("2"), {"condition": RegexMatchCondition.name, "value": "2"}),
    ])
    def test_from_json(self, condition, condition_json):
        new_condition = condition.__class__.from_json(condition_json)
        assert isinstance(new_condition, condition.__class__)
        for attr in condition.__dict__:
            assert getattr(new_condition, attr) == getattr(condition, attr)

    @pytest.mark.parametrize("condition, value, err_msg", [
        (ContainsCondition, 1, "Invalid argument type '{}' for string condition.".format(int)),
        (NotContainsCondition, [], "Invalid argument type '{}' for string condition.".format(list)),
        (EqualsCondition, {}, "Invalid argument type '{}' for string condition.".format(dict)),
        (NotEqualsCondition, None, "Invalid argument type '{}' for string condition.".format(type(None))),
        (StartsWithCondition, {1, }, "Invalid argument type '{}' for string condition.".format(set)),
        (EndsWithCondition, (), "Invalid argument type '{}' for string condition.".format(tuple)),
        (RegexMatchCondition, "(", "Argument '{}' not a valid regexp string.".format("(")),
    ])
    def test_type_error(self, condition, value, err_msg):
        with pytest.raises(TypeError) as err:
            condition(value)
        assert str(err.value) == err_msg

    @pytest.mark.parametrize("condition, what, result", [
        (ContainsCondition("b"), "abc", True),
        (ContainsCondition("b"), "cde", False),
        (NotContainsCondition("b"), "abc", False),
        (NotContainsCondition("b"), "cde", True),
        (EqualsCondition("abc"), "abc", True),
        (EqualsCondition("b"), "cde", False),
        (NotEqualsCondition("abc"), "abc", False),
        (NotEqualsCondition("b"), "cde", True),
        (StartsWithCondition("ab"), "abc", True),
        (StartsWithCondition("ab"), "ab", True),
        (StartsWithCondition("ab"), "cab", False),
        (EndsWithCondition("ab"), "abc", False),
        (EndsWithCondition("ab"), "ab", True),
        (EndsWithCondition("ab"), "cab", True),
        (RegexMatchCondition(".*"), "foo", True),
        (RegexMatchCondition("abc"), "abc", True),
        (RegexMatchCondition("abc"), "abd", False),
        (RegexMatchCondition(r"[\d\w]+"), "567asd", True),
        (RegexMatchCondition(""), "", True),
        (RegexMatchCondition(r"^python\?exe"), "python?exe", True),
        (RegexMatchCondition(r"^python?exe"), "python?exe", False),
    ])
    def test_is_satisfied(self, condition, what, result):
        assert condition.is_satisfied(what) == result
