"""
    MongoDB storage
"""

import json
import logging

from pymongo.errors import DuplicateKeyError

from pyabac.common.exceptions import PolicyExistsError
from .abc import Storage, DEFAULT_POLICY_COLLECTION
from ..policy import Policy

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
        try:
            self.collection.insert_one(self._prepare_doc(policy))
        except DuplicateKeyError:
            log.error('Error trying to create already existing policy with UID=%s.', policy.uid)
            raise PolicyExistsError(policy.uid)
        log.info('Added Policy: %s', policy)

    def get(self, uid):
        ret = self.collection.find_one(uid)
        if not ret:
            return None
        return self._prepare_from_doc(ret)

    def get_all(self, limit, offset, collection=DEFAULT_POLICY_COLLECTION):
        self._check_limit_and_offset(limit, offset)
        cur = self.collection.find({"collection": collection}, limit=limit, skip=offset)
        for doc in cur:
            yield self._prepare_from_doc(doc)

    def get_for_inquiry(self, inquiry):
        cur = self.collection.find({"collection": inquiry.collection})
        for doc in cur:
            yield self._prepare_from_doc(doc)

    def update(self, policy):
        uid = policy.uid
        self.collection.update_one(
            {'_id': uid},
            {"$set": self._prepare_doc(policy)},
            upsert=False)
        log.info('Updated Policy with UID=%s. New value is: %s', uid, policy)

    def delete(self, uid):
        self.collection.delete_one({'_id': uid})
        log.info('Deleted Policy with UID=%s.', uid)

    @staticmethod
    def _prepare_from_doc(doc):
        """
        Prepare Policy object as a return from MongoDB.
        """
        policy_json = json.loads(doc['policy'])
        return Policy.from_json(policy_json)

    @staticmethod
    def _prepare_doc(policy):
        """
        Prepare Policy object as a document for insertion.
        """
        policy_json = policy.to_json()
        return {'_id': policy.uid, 'policy': json.dumps(policy_json), 'collection': policy.collection}
