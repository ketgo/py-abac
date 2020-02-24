"""
    SQL Storage implementation
"""

import logging

from ..base import StorageBase
from ...exceptions import PolicyExistsError
from ...policy import Policy

LOG = logging.getLogger(__name__)


class SQLStorage(StorageBase):
    """
        Stores and retrieves policies from SQL database

        :param scoped_session: SQL Alchemy scoped session
    """

    def __init__(self, scoped_session):
        self.session = scoped_session

    def get(self, uid: str) -> Policy:
        raise PolicyExistsError
