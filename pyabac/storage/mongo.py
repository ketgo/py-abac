"""
    Implementation of vakt `MongoStorage` with policy scoping support
"""

import logging

import bson.json_util as b_json
from vakt.storage.mongo import MongoStorage as VaktMongoStorage

from .abc import Storage, DEFAULT_POLICY_SCOPE
from ..policy import Policy

log = logging.getLogger(__name__)


class MongoStorage(Storage, VaktMongoStorage):

    def get(self, uid, scope=DEFAULT_POLICY_SCOPE):
        ret = self.collection.find_one({'_id': self.__get__id(uid, scope)})
        if not ret:
            return None
        return self.__prepare_from_doc(ret)

    def get_all(self, limit, offset, scope=DEFAULT_POLICY_SCOPE):
        self._check_limit_and_offset(limit, offset)
        cur = self.collection.find({"scope": scope}, limit=limit, skip=offset)
        return self.__feed_policies(cur)

    def find_for_inquiry(self, inquiry, checker=None):
        q_filter = self._create_filter(inquiry, checker)
        q_filter["scope"] = inquiry.scope
        cur = self.collection.find(q_filter)
        return self.__feed_policies(cur)

    def update(self, policy):
        uid = policy.uid
        scope = policy.scope
        self.collection.update_one(
            {'_id': self.__get__id(uid, scope)},
            {"$set": self.__prepare_doc(policy)},
            upsert=False)
        log.info('Updated Policy with UID=%s. New value is: %s', uid, policy)

    def delete(self, uid, scope=DEFAULT_POLICY_SCOPE):
        self.collection.delete_one({'_id': self.__get__id(uid, scope)})
        log.info('Deleted Policy with UID={} within scope={}.'.format(uid, scope))

    @staticmethod
    def __get__id(uid, scope):
        return "{}:{}".format(uid, scope)

    @staticmethod
    def __prepare_doc(policy):
        """
        Prepare Policy object as a document for insertion.
        """
        # todo - add dict inheritance
        doc = b_json.loads(policy.to_json())
        doc['_id'] = MongoStorage.__get__id(policy.uid, policy.scope)
        return doc

    @staticmethod
    def __prepare_from_doc(doc):
        """
        Prepare Policy object as a return from MongoDB.
        """
        # todo - add dict inheritance
        del doc['_id']
        return Policy.from_json(b_json.dumps(doc))
