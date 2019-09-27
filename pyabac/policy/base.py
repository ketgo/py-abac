"""
    Policy Base Class
"""

from abc import ABCMeta, abstractmethod


class PolicyBase(metaclass=ABCMeta):
    """
        Base class for policy
    """

    @abstractmethod
    def fits(self, inquiry):
        """
            Check if the policy fits the inquiry

            :param inquiry: inquiry object
            :return: True if true else False
        """
