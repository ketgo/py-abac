"""
    Unit test evaluation context
"""

import pytest

from py_abac.context import EvaluationContext
from py_abac.exceptions import InvalidAccessControlElementError, InvalidAttributePathError
from py_abac.provider.base import AttributeProvider
from py_abac.request import AccessRequest


class EmailAttributeProvider(AttributeProvider):

    def get_attribute_value(self, ace, attribute_path, ctx):
        if ace == "subject" and attribute_path == "$.email":
            return "carl@gmail.com"


class FaultyAttributeProvider(AttributeProvider):

    def get_attribute_value(self, ace, attribute_path, ctx):
        # This will test for infinite recessive loops
        return ctx.get_attribute_value(ace, attribute_path)


def test_create():
    request_json = {
        "subject": {
            "id": "a",
            "attributes": {
                "firstName": "Carl",
                "lastName": "Right",
                "middleName": ""
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
    request = AccessRequest.from_json(request_json)
    context = EvaluationContext(request)
    assert context.subject_id == request._subject_id
    assert context.resource_id == request._resource_id
    assert context.action_id == request._action_id
    assert context._other_providers == []
    assert context.ace is None
    assert context.attribute_path is None

    context.ace = "subject"
    context.attribute_path = "$.firstName"
    assert context.attribute_value == "Carl"
    context.attribute_path = "$.lastName"
    assert context.attribute_value == "Right"
    context.attribute_path = "$.middleName"
    assert context.attribute_value == ""

    context.ace = "resource"
    context.attribute_path = "$.name"
    assert context.attribute_value == "Calendar"


def test_get_attribute_value():
    request_json = {
        "subject": {
            "id": "a",
            "attributes": {
                "firstName": "Carl",
                "lastName": "Right",
                "middleName": ""
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
    request = AccessRequest.from_json(request_json)
    context = EvaluationContext(request, providers=[EmailAttributeProvider()])
    assert context.get_attribute_value("subject", "$.firstName") == "Carl"
    assert context.get_attribute_value("subject", "$.middleName") == ""
    assert context.get_attribute_value("subject", "$.email") == "carl@gmail.com"
    assert context.get_attribute_value("resource", "$.name") == "Calendar"
    assert context.get_attribute_value("context", "$.ip") is None


def test_attribute_provider_infinite_recursion():
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
    request = AccessRequest.from_json(request_json)
    context = EvaluationContext(request, providers=[FaultyAttributeProvider()])
    assert context.get_attribute_value("subject", "$.email") is None

    context = EvaluationContext(request, providers=[FaultyAttributeProvider(),
                                                    EmailAttributeProvider(),
                                                    FaultyAttributeProvider(),
                                                    EmailAttributeProvider(),
                                                    FaultyAttributeProvider()])
    assert context.get_attribute_value("subject", "$.age") is None


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
    request = AccessRequest.from_json(request_json)
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
