"""
    Test inquiry
"""

import pytest

from pyabac.common.constants import DEFAULT_POLICY_COLLECTION
from pyabac.common.exceptions import InquiryCreationError
from pyabac.inquiry import Inquiry


class TestInquiry(object):

    @pytest.mark.parametrize("inquiry, inquiry_json", [
        (Inquiry(),
         {"subject": {},
          "resource": {},
          "action": {},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(subject={"name": "test"}),
         {"subject": {"name": "test"},
          "resource": {},
          "action": {},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(resource={"name": "test"}),
         {"subject": {},
          "resource": {"name": "test"},
          "action": {},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(action={"name": "test"}),
         {"subject": {},
          "resource": {},
          "action": {"name": "test"},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(context={"name": "test"}),
         {"subject": {},
          "resource": {},
          "action": {},
          "context": {"name": "test"},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(collection="test"),
         {"subject": {},
          "resource": {},
          "action": {},
          "context": {},
          "collection": "test"}),
    ])
    def test_to_json(self, inquiry, inquiry_json):
        assert inquiry.to_json() == inquiry_json

    @pytest.mark.parametrize("inquiry, inquiry_json", [
        (Inquiry(),
         {"subject": {},
          "resource": {},
          "action": {},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(subject={"name": "test"}),
         {"subject": {"name": "test"},
          "resource": {},
          "action": {},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(resource={"name": "test"}),
         {"subject": {},
          "resource": {"name": "test"},
          "action": {},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(action={"name": "test"}),
         {"subject": {},
          "resource": {},
          "action": {"name": "test"},
          "context": {},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(context={"name": "test"}),
         {"subject": {},
          "resource": {},
          "action": {},
          "context": {"name": "test"},
          "collection": DEFAULT_POLICY_COLLECTION}),
        (Inquiry(collection="test"),
         {"subject": {},
          "resource": {},
          "action": {},
          "context": {},
          "collection": "test"}),
    ])
    def test_from_json(self, inquiry, inquiry_json):
        new_inquiry = inquiry.__class__.from_json(inquiry_json)
        assert isinstance(new_inquiry, inquiry.__class__)
        for attr in inquiry.__dict__:
            assert getattr(new_inquiry, attr) == getattr(inquiry, attr)

    @pytest.mark.parametrize("args", [
        {"subject": "test",
         "resource": {},
         "action": {},
         "context": {},
         "collection": "test"},
        {"subject": {},
         "resource": "test",
         "action": {},
         "context": {},
         "collection": "test"},
        {"subject": {},
         "resource": {},
         "action": "test",
         "context": {},
         "collection": "test"},
        {"subject": {},
         "resource": {},
         "action": {},
         "context": "test",
         "collection": "test"},
        {"subject": {},
         "resource": {},
         "action": {},
         "context": {},
         "collection": {"test": True}},
    ])
    def test_create_error(self, args):
        with pytest.raises(InquiryCreationError):
            Inquiry(**args)

    @pytest.mark.parametrize("inquiry_json", [
        {"subject": "test",
         "resource": {},
         "action": {},
         "context": {},
         "collection": "test"},
        {"subject": {},
         "resource": "test",
         "action": {},
         "context": {},
         "collection": "test"},
        {"subject": {},
         "resource": {},
         "action": "test",
         "context": {},
         "collection": "test"},
        {"subject": {},
         "resource": {},
         "action": {},
         "context": "test",
         "collection": "test"},
        {"subject": {},
         "resource": {},
         "action": {},
         "context": {},
         "collection": {"test": True}},
    ])
    def test_create_from_json_error(self, inquiry_json):
        with pytest.raises(InquiryCreationError):
            Inquiry.from_json(inquiry_json)
