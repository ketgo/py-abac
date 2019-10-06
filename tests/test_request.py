"""
    Unit test for authorization request
"""

import pytest

from pyabac.exceptions import RequestCreateError, InvalidAccessControlElementError, InvalidAttributePathError
from pyabac.request import Request


def test_create():
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
    request = Request(request_json)

    assert request_json["subject"]["id"] == request.subject_id
    assert request_json["resource"]["id"] == request.resource_id
    assert request_json["action"]["id"] == request.action_id


def test_get_value():
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
    request = Request(request_json)

    assert request_json["subject"]["attributes"]["firstName"] == request.get_value("subject", "$.firstName")
    assert request_json["subject"]["attributes"]["lastName"] == request.get_value("subject", "$.lastName")
    assert request.get_value("subject", "$.test") is None
    assert request_json["resource"]["attributes"]["name"] == request.get_value("resource", "$.name")
    assert request.get_value("resource", "$.test") is None
    assert request.get_value("action", "$.test") is None
    assert request.get_value("context", "$.test") is None


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
    request = Request(request_json)
    with pytest.raises(InvalidAccessControlElementError):
        request.get_value("test", "$.test")


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
    request = Request(request_json)
    with pytest.raises(InvalidAttributePathError):
        request.get_value("subject", ")")


@pytest.mark.parametrize("request_json", [
    {
        "subject": {
            "attributes": {}
        },
        "resource": {
            "id": "a",
            "attributes": {}
        },
        "action": {
            "id": "",
            "attributes": {}
        },
        "context": {}
    },
    {
        "subject": {
            "id": "a",
            "attributes": {}
        },
        "resource": {
            "attributes": {}
        },
        "action": {
            "id": "",
            "attributes": {}
        },
        "context": {}
    },
    {
        "subject": {
            "id": "a",
            "attributes": {}
        },
        "resource": {
            "id": "a",
            "attributes": {}
        },
        "action": {
            "attributes": {}
        },
        "context": {}
    },
    {
        "subject": {
            "id": 1,
            "attributes": {}
        },
        "resource": {
            "id": "a",
            "attributes": {}
        },
        "action": {
            "id": "1",
            "attributes": {}
        },
        "context": {}
    },
    {
        "subject": {
            "id": "1",
            "attributes": {}
        },
        "resource": {
            "id": 1,
            "attributes": {}
        },
        "action": {
            "id": "1",
            "attributes": {}
        },
        "context": {}
    },
    {
        "subject": {
            "id": "1",
            "attributes": []
        },
        "resource": {
            "id": "1",
            "attributes": {}
        },
        "action": {
            "id": "1",
            "attributes": {}
        },
        "context": {}
    },
    {
        "subject": {
            "id": "1",
            "attributes": {}
        },
        "resource": {
            "id": 1,
            "attributes": {}
        },
        "context": {}
    }
])
def test_create_error(request_json):
    with pytest.raises(RequestCreateError):
        Request(request_json)
