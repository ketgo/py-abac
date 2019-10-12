"""
    Attribute provider base class
"""

from abc import ABCMeta, abstractmethod


class AttributeProvider(metaclass=ABCMeta):
    """
        Attribute provider interface
    """

    @abstractmethod
    def get_attribute_value(self, ace: str, attribute_path: str):
        """
            Get attribute value for given access control element and attribute path. If
            attribute not found then returns None.

            :param ace: Access control element
            :param attribute_path: attribute path in ObjectPath format
            :return: attribute value
        """
        raise NotImplementedError()
