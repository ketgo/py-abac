"""
    Wrapper on vakt `Storage` core components to support policy scoping
"""

from vakt.storage.abc import Storage as VaktStorage
from abc import abstractmethod
from ..constants import DEFAULT_POLICY_SCOPE


class Storage(VaktStorage):

    @abstractmethod
    def get(self, uid, scope=DEFAULT_POLICY_SCOPE):
        """Get specific policy within a given scope"""
        pass

    @abstractmethod
    def get_all(self, limit, offset, scope=DEFAULT_POLICY_SCOPE):
        """
        Retrieve all the policies within a window within a given scope.

        Returns Iterable
        """
        pass

    @abstractmethod
    def delete(self, uid, scope=DEFAULT_POLICY_SCOPE):
        """Delete a policy within a given scope"""
        pass
