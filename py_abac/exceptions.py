"""
    All py_abac exceptions
"""


class RequestCreateError(Exception):
    """
        Error occurred during Request creation.
    """
    pass


class PolicyCreateError(Exception):
    """
        Error occurred during Policy creation.
    """
    pass


class PolicyExistsError(Exception):
    """
        Error when the already existing policy is attempted to be created by Storage
    """

    def __init__(self, uid):
        super().__init__("Conflicting UID = '{}'".format(uid))


class InvalidAccessControlElementError(Exception):
    """
        Error occurred when accessing invalid access control element
    """

    def __init__(self, element):
        super().__init__(
            "Invalid access control element '{}'. Allowed values are "
            "'subject', 'resource', 'action', and 'context'".format(element)
        )


class InvalidAttributePathError(Exception):
    """
        Error occurred when invalid attribute path is found
    """

    def __init__(self, path):
        super().__init__(
            "Invalid attribute path '{}'. Path required in ObjectPath format.".format(path)
        )
