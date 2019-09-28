"""
    Benchmark test for json query packages
"""

import pytest
from jsonpath_ng import parse
import pyjq
import objectpath


N = 100


def runs_n(n, func, *args):
    rvalue = []
    for _ in range(n):
        rvalue += func(*args)
    return rvalue


@pytest.mark.parametrize('path, json, results', [
    ("$", {"a": {"b": [1, {"c": 2}]}}, [{"a": {"b": [1, {"c": 2}]}}]),
    ("$.a", {"a": {"b": [1, {"c": 2}]}}, [{"b": [1, {"c": 2}]}]),
])
def test_jsonpath(path, json, results, benchmark):
    matches = benchmark(runs_n, N, parse(path).find, json)
    assert all(match.value in results for match in matches)


@pytest.mark.parametrize('path, json, results', [
    (".", {"a": {"b": [1, {"c": 2}]}}, [{"a": {"b": [1, {"c": 2}]}}]),
    (".a", {"a": {"b": [1, {"c": 2}]}}, [{"b": [1, {"c": 2}]}]),
])
def test_pyjq(path, json, results, benchmark):
    matches = benchmark(runs_n, N, pyjq.all, path, json)
    assert all(match in results for match in matches)


@pytest.mark.parametrize('path, json, results', [
    ("$.*", {"a": {"b": [1, {"c": 2}]}}, [{"a": {"b": [1, {"c": 2}]}}]),
    ("$.a", {"a": {"b": [1, {"c": 2}]}}, [{"b": [1, {"c": 2}]}]),
])
def test_objectpath(path, json, results, benchmark):
    def _find(func, x):
        return [func(x)]
    matches = benchmark(runs_n, N, _find, objectpath.Tree(json).execute, path)
    assert all(match in results for match in matches)


if __name__ == '__main__':
    pytest.main()
