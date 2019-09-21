"""
    MongoDB storage
"""

import logging

from .abc import Storage, DEFAULT_POLICY_COLLECTION

DEFAULT_DB = 'security'
DEFAULT_COLLECTION = 'policies'

log = logging.getLogger(__name__)


class MongoStorage(Storage):
    """
        Stores all policies in MongoDB
    """

    def __init__(self, client, db_name=DEFAULT_DB, collection=DEFAULT_COLLECTION):
        self.client = client
        self.database = self.client[db_name]
        self.collection = self.database[collection]

    def add(self, policy):
        pass

    def get(self, uid):
        pass

    def get_all(self, limit, offset, collection=DEFAULT_POLICY_COLLECTION):
        pass

    def get_for_inquiry(self, inquiry):
        pass

    def update(self, policy):
        pass

    def delete(self, uid):
        pass
