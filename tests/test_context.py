"""
    Unit test evaluation context
"""

import pytest

from pyabac.context import EvaluationContext
from pyabac.request import Request, InvalidAccessControlElementError, InvalidAttributePathError


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
    context = EvaluationContext(request)
    assert context.request == request
    assert context.ace is None
    assert context.attribute_path is None

    context.ace = "subject"
    context.attribute_path = "$.firstName"
    assert context.attribute_value == "Carl"
    context.attribute_path = "$.lastName"
    assert context.attribute_value == "Right"

    context.ace = "resource"
    context.attribute_path = "$.name"
    assert context.attribute_value == "Calendar"


def test_attribute_value_raises():
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
    context = EvaluationContext(request)
    with pytest.raises(InvalidAccessControlElementError):
        _ = context.attribute_value

    context.ace = "test"
    with pytest.raises(InvalidAccessControlElementError):
        _ = context.attribute_value

    context.ace = "subject"
    context.attribute_path = ")"
    with pytest.raises(InvalidAttributePathError):
        _ = context.attribute_value
