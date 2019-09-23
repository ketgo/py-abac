"""
    This file contains implementation fo the ABAC engine
"""
from .inquiry import Inquiry
from .storage.abc import Storage


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
        filtered = [policy for policy in policies if
                    policy.fits(inquiry) and self._check_context_restriction(policy, inquiry)]

        # no policies -> deny access!
        # if we have 2 or more similar policies - all of them should have allow effect, otherwise -> deny access!
        return len(filtered) > 0 and all(p.allow_access() for p in filtered)

    @staticmethod
    def _check_context_restriction(policy, inquiry):
        """
            Check if context restriction in the policy is satisfied for a given inquiry's context.
        """
        for key, condition in policy.context.items():
            # If at least one rule is not present in Inquiry's context -> deny access
            try:
                ctx_value = inquiry.context[key]
            except KeyError:
                return False
            # If at least one rule provided in Inquiry's context is not satisfied -> deny access
            if not condition.is_satisfied(ctx_value):
                return False

        return True
