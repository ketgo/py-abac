"""
    Unit test for request attribute provider
"""

import pytest

from py_abac.context import EvaluationContext
from py_abac.exceptions import InvalidAccessControlElementError, InvalidAttributePathError
from py_abac.provider.request import RequestAttributeProvider
from py_abac.request import Request


def test_get_attribute_value():
    request_json = {
        "subject": {
            "id": "a",
            "attributes": {
                "firstName": "Carl",
                "lastName": "Right"
            }
        },
        "resource": {
            "id": "a",
            "attributes": {
                "name": "Calendar"
            }
        },
        "action": {
            "id": "",
            "attributes": {}
        },
        "context": {}
    }
    request = Request.from_json(request_json)
    ctx = EvaluationContext(request)
    provider = RequestAttributeProvider(request)

    assert request_json["subject"]["attributes"]["firstName"] == provider.get_attribute_value("subject", "$.firstName",
                                                                                              ctx)
    assert request_json["subject"]["attributes"]["lastName"] == provider.get_attribute_value("subject", "$.lastName",
                                                                                             ctx)
    assert provider.get_attribute_value("subject", "$.test", ctx) is None
    assert request_json["resource"]["attributes"]["name"] == provider.get_attribute_value("resource", "$.name", ctx)
    assert provider.get_attribute_value("resource", "$.test", ctx) is None
    assert provider.get_attribute_value("action", "$.test", ctx) is None
    assert provider.get_attribute_value("context", "$.test", ctx) is None


def test_invalid_ace_error():
    request_json = {
        "subject": {
            "id": "a",
            "attributes": {
                "firstName": "Carl",
                "lastName": "Right"
            }
        },
        "resource": {
            "id": "a",
            "attributes": {
                "name": "Calendar"
            }
        },
        "action": {
            "id": "",
            "attributes": {}
        },
        "context": {}
    }
    request = Request.from_json(request_json)
    ctx = EvaluationContext(request)
    provider = RequestAttributeProvider(request)
    with pytest.raises(InvalidAccessControlElementError):
        provider.get_attribute_value("test", "$.test", ctx)


def test_invalid_attribute_path_error():
    request_json = {
        "subject": {
            "id": "a",
            "attributes": {
                "firstName": "Carl",
                "lastName": "Right"
            }
        },
        "resource": {
            "id": "a",
            "attributes": {
                "name": "Calendar"
            }
        },
        "action": {
            "id": "",
            "attributes": {}
        },
        "context": {}
    }
    request = Request.from_json(request_json)
    ctx = EvaluationContext(request)
    provider = RequestAttributeProvider(request)
    with pytest.raises(InvalidAttributePathError):
        provider.get_attribute_value("subject", ")", ctx)
