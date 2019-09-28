"""
    This file contains implementation fo the ABAC engine
"""

from pyabac.checker import Checker
from pyabac.inquiry import Inquiry
from pyabac.storage.abc import Storage


class Guard(object):
    """
        Attribute Based Access Control (ABAC) evaluation engine
    """

    def __init__(self, storage):
        """
            Initialize guard object

            :param storage: policy storage
        """
        if not isinstance(storage, Storage):
            raise TypeError("Invalid type '{}' for storage.".format(type(storage)))
        self.storage = storage

    def is_allowed(self, inquiry):
        """
            Check if inquiry is allowed

            :param inquiry: inquiry object
            :return: True if allowed
        """
        if not isinstance(inquiry, Inquiry):
            raise TypeError("Invalid type '{}' for inquiry.".format((type(inquiry))))

        # Get policies for inquiry from storage
        policies = self.storage.get_for_inquiry(inquiry)

        # filter for matching policies
        checker = Checker(inquiry)
        filtered = [policy for policy in policies if checker.fits(policy)]

        # no policies -> deny access!
        # if we have 2 or more similar policies - all of them should have allow effect, otherwise -> deny access!
        return len(filtered) > 0 and all(p.allow_access() for p in filtered)
