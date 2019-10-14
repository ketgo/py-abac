"""
    Unit test for authorization request
"""

import pytest

from py_abac.exceptions import RequestCreateError
from py_abac.request import Request


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
    request = Request.from_json(request_json)

    assert request_json["subject"]["id"] == request._subject_id
    assert request_json["resource"]["id"] == request._resource_id
    assert request_json["action"]["id"] == request._action_id


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
        Request.from_json(request_json)
