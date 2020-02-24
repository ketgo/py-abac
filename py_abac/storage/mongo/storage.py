"""
    MongoDB storage implementation
"""

import logging

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from .model import PolicyModel
from ..base import StorageBase
from ...exceptions import PolicyExistsError
from ...policy import Policy

DEFAULT_DB = 'py_abac'
DEFAULT_COLLECTION = 'py_abac_policies'

LOG = logging.getLogger(__name__)


class MongoStorage(StorageBase):
    """
        Stores and retrieves policies from MongoDB
    """

    def __init__(
            self,
            client: MongoClient,
            db_name: str = DEFAULT_DB,
            collection: str = DEFAULT_COLLECTION
    ):
        self.client = client
        self.database = self.client[db_name]
        self.collection = self.database[collection]

    def add(self, policy: Policy):
        try:
            self.collection.insert_one(PolicyModel.from_policy(policy).to_doc())
        except DuplicateKeyError:
            LOG.error('Error trying to create already existing policy with UID=%s.', policy.uid)
            raise PolicyExistsError(policy.uid)
        LOG.info('Added Policy: %s', policy)

    def get(self, uid: str):
        doc = self.collection.find_one(uid)
        if not doc:
            return None
        return PolicyModel.from_doc(doc).to_policy()

    def get_all(self, limit: int, offset: int):
        self._check_limit_and_offset(limit, offset)
        cur = self.collection.find({}, limit=limit, skip=offset)
        for doc in cur:
            yield PolicyModel.from_doc(doc).to_policy()

    def get_for_target(self, subject_id: str, resource_id: str, action_id: str):
        pipeline = PolicyModel.get_aggregate_pipeline(subject_id, resource_id, action_id)
        cur = self.collection.aggregate(pipeline)
        for doc in cur:
            yield PolicyModel.from_doc(doc).to_policy()

    def update(self, policy: Policy):
        uid = policy.uid
        self.collection.update_one(
            {'_id': uid},
            {"$set": PolicyModel.from_policy(policy).to_doc()},
            upsert=False
        )
        LOG.info('Updated Policy with UID=%s. New value is: %s', uid, policy)

    def delete(self, uid: str):
        self.collection.delete_one({'_id': uid})
        LOG.info('Deleted Policy with UID=%s.', uid)
