"""
    All pyabac exceptions
"""


class PolicyCreationError(Exception):
    """
        Error occurred during Policy creation.
    """
    pass


class PolicyExistsError(Exception):
    """
        Error when the already existing policy is attempted to be created by Storage
    """

    def __init__(self, uid):
        super().__init__('Conflicting UID = %s' % uid)


class ConditionCreationError(Exception):
    """
        Error occurred during condition creation.
    """
    pass
