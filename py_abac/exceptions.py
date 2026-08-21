"""
    All py_abac exceptions
"""


class RequestCreateError(Exception):
    """
        Error occurred during Request creation.
    """


class PolicyCreateError(Exception):
    """
        Error occurred during Policy creation.
    """


class PolicyExistsError(Exception):
    """
        Error when the already existing policy is attempted to be created by Storage
    """

    def __init__(self, uid):
        super().__init__(f"Conflicting UID = '{uid}'")


class InvalidAccessControlElementError(Exception):
    """
        Error occurred when accessing invalid access control element
    """

    def __init__(self, element):
        super().__init__(
            f"Invalid access control element '{element}'. Allowed values are "
            "'subject', 'resource', 'action', and 'context'"
        )


class InvalidAttributePathError(Exception):
    """
        Error occurred when invalid attribute path is found
    """

    def __init__(self, path):
        super().__init__(
            f"Invalid attribute path '{path}'. Path required in ObjectPath format."
        )
