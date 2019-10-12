"""
    Unit test for request attribute provider
"""

import pytest

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
    provider = RequestAttributeProvider(Request.from_json(request_json))

    assert request_json["subject"]["attributes"]["firstName"] == provider.get_attribute_value("subject", "$.firstName")
    assert request_json["subject"]["attributes"]["lastName"] == provider.get_attribute_value("subject", "$.lastName")
    assert provider.get_attribute_value("subject", "$.test") is None
    assert request_json["resource"]["attributes"]["name"] == provider.get_attribute_value("resource", "$.name")
    assert provider.get_attribute_value("resource", "$.test") is None
    assert provider.get_attribute_value("action", "$.test") is None
    assert provider.get_attribute_value("context", "$.test") is None


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
    provider = RequestAttributeProvider(Request.from_json(request_json))
    with pytest.raises(InvalidAccessControlElementError):
        provider.get_attribute_value("test", "$.test")


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
    provider = RequestAttributeProvider(Request.from_json(request_json))
    with pytest.raises(InvalidAttributePathError):
        provider.get_attribute_value("subject", ")")
