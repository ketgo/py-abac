"""
    Unit test evaluation context
"""

import pytest

from py_abac.context import EvaluationContext
from py_abac.request import Request, InvalidAccessControlElementError, InvalidAttributePathError


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
    assert context.subject_id == request._subject_id
    assert context.resource_id == request._resource_id
    assert context.action_id == request._action_id
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


def test_create_type_error():
    with pytest.raises(TypeError):
        EvaluationContext(None)


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
