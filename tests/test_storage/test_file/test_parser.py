"""
    Tests for JSON dot notation parser
"""

import pytest

from py_abac.storage.file.parser import JSONDotParser


@pytest.fixture
def mock_dict():
    return {
        "a": 1,
        "b": [{"c": 2}, {"c": 3}, {"d": 4}]
    }


@pytest.fixture
def mock_str():
    return '"a":1,"b.0.c":2,"b.1.c":3,"b.2.d":4'


def test_dumps(mock_dict, mock_str):
    assert mock_str == JSONDotParser.dumps(mock_dict)


def test_loads(mock_dict, mock_str):
    assert mock_dict == JSONDotParser.loads(mock_str)
