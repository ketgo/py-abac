"""
    Simple memory storage
"""
import logging

from ..exceptions import PolicyExistsError
from ..storage.abc import Storage, DEFAULT_POLICY_COLLECTION

log = logging.getLogger(__name__)


class MemoryStorage(Storage):

    def __init__(self):
        self._uid_policies_map = {}
        self._collection_policies_map = {}

    def add(self, policy):
        uid = str(policy.uid)
        collection = str(policy.collection)
        if uid in self._uid_policies_map:
            raise PolicyExistsError(uid)
        self._uid_policies_map[uid] = policy
        if collection in self._collection_policies_map:
            self._collection_policies_map[collection][uid] = policy
        else:
            self._collection_policies_map[collection] = {uid: policy}

    def get(self, uid):
        return self._uid_policies_map.get(uid)

    def get_all(self, limit, offset, collection=DEFAULT_POLICY_COLLECTION):
        self._check_limit_and_offset(limit, offset)
        policies = list(self._collection_policies_map.get(collection, {}).values())
        for policy in policies[offset:(offset + limit)]:
            yield policy

    def get_for_inquiry(self, inquiry):
        policies = self._collection_policies_map.get(inquiry.collection, {}).values()
        for policy in policies:
            yield policy

    def update(self, policy):
        uid = str(policy.uid)
        collection = str(policy.collection)
        self._uid_policies_map[uid] = policy
        self._collection_policies_map[collection][uid] = policy

    def delete(self, uid):
        if uid in self._uid_policies_map:
            self._uid_policies_map.pop(uid)
        for collection in self._collection_policies_map:
            if uid in self._collection_policies_map[collection]:
                self._collection_policies_map[collection].pop(uid)
