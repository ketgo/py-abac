"""
    Test storage utility methods
"""

import fnmatch

import pytest

from py_abac.storage.utils import get_sub_wildcard_queries, get_all_wildcard_queries


@pytest.mark.parametrize("query, sub_queries", [
    ("a", ["a"]),
    ("*", ["*"]),

    ("ab", ["ab"]),
    ("a*", ["a*"]),
    ("*a", ["*a"]),
    ("**", ["*"]),

    ("abc", ["abc"]),
    ("*ab", ["*ab"]),
    ("a*b", ["a*", "*b"]),
    ("ab*", ["ab*"]),
    ("**a", ["*a"]),
    ("*a*", ["*a*"]),
    ("a**", ["a*"]),
    ("***", ["*"]),

    ("abcd", ["abcd"]),
    ("*abc", ["*abc"]),
    ("a*bc", ["a*", "*bc"]),
    ("ab*c", ["ab*", "*c"]),
    ("abc*", ["abc*"]),
    ("**ab", ["*ab"]),
    ("*a*b", ["*a*", "*b"]),
    ("*ab*", ["*ab*"]),
    ("a**b", ["a*", "*b"]),
    ("a*b*", ["a*", "*b*"]),
    ("ab**", ["ab*"]),
    ("***a", ["*a"]),
    ("a***", ["a*"]),
    ("****", ["*"]),
])
def test_get_sub_wildcard_queries(query, sub_queries):
    test_string = "abcd"
    assert get_sub_wildcard_queries(query) == sub_queries
    assert fnmatch.fnmatch(test_string, query) == all(
        fnmatch.fnmatch(test_string, x) for x in sub_queries
    )


@pytest.mark.parametrize("string, queries", [
    ("a", ['a', '*', '*a*', 'a*', '*a']),
    ("ab", ['ab', '*', '*a*', 'a*', '*b', '*b*', '*ab*', 'ab*', '*ab']),
    ("abc", ['abc', '*', '*a*', 'a*', '*b*', '*c', '*c*', '*ab*', 'ab*', '*bc', '*bc*', '*abc*', 'abc*', '*abc']),
    ("abcd",
     ['abcd', '*', '*a*', 'a*', '*b*', '*c*', '*d', '*d*', '*ab*', 'ab*', '*bc*', '*cd', '*cd*', '*abc*', 'abc*',
      '*bcd',
      '*bcd*', '*abcd*', 'abcd*', '*abcd'])
])
def test__get_all_wildcard_queries(string, queries):
    assert sorted(get_all_wildcard_queries(string)) == sorted(queries)
    assert all(fnmatch.fnmatch(string, x) for x in queries)
