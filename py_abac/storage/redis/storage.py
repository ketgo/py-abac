"""
    Redis policy storage
"""

import logging
from typing import Generator

from redis import Redis

from ..base import Storage
from ...exceptions import PolicyExistsError
from ...policy import Policy

LOG = logging.getLogger(__name__)

DEFAULT_HASH_VALUE = "py_abac_policies"


class RedisStorage(Storage):
    """
        Redis policy storage backend.

        :param client: redis client.
        :param hash_value: hash value under which policies are
            stored in database.
    """

    def __init__(self, client: Redis, hash_value: str = None):
        self.client = client
        self._hash = hash_value or DEFAULT_HASH_VALUE

    def add(self, policy: Policy):
        """
            Store a policy
        """
        rvalue = self.client.hsetnx(self._hash, policy.uid, policy.to_json())
        if rvalue == 0:
            LOG.error('Error trying to create already existing policy with UID=%s.', policy.uid)
            raise PolicyExistsError(policy.uid)
        LOG.info('Added Policy: %s', policy)

    def get(self, uid: str) -> Policy:
        """
            Get specific policy
        """
        rvalue = self.client.hget(self._hash, uid)
        return rvalue.value()

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        """
            Retrieve all the policies within a window
        """
        self._check_limit_and_offset(limit, offset)
        count = 0
        cursor = offset
        while count < limit and cursor != 0:
            cursor, policies = self.client.hscan(self._hash, cursor=cursor, count=1)
            for policy in policies:
                yield policy

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        """
            Get all policies for given target IDs.
        """
        # NOTE: Currently all policies are returned for evaluation by PDP.
        # TODO: Create topologically sorted graph index for filtered retrieval.
        for policy in self.client.hgetall(self._hash):
            yield policy

    def update(self, policy: Policy):
        """
            Update a policy

            NOTE: The lua script is used to make sure an update
                operation occurs instead of upsert.
        """
        uid = policy.uid
        lua = """
                local exists = redis.call('HEXISTS', KEYS[1], ARGV[1])
                if exists == 1 then
                    return redis.call('HSET', KEYS[1], ARGV[1], ARGV[2])
                end
                return 0
                """
        update_policy = self.client.register_script(lua)
        try:
            rvalue = update_policy(keys=[self._hash], args=[uid, policy.to_json()])
            if rvalue != 0:
                LOG.info('Updated Policy with UID=%s. New value is: %s', uid, policy)
        except Exception as err:
            LOG.exception('Error trying to update policy with UID=%s.', uid)
            raise err

    def delete(self, uid: str):
        """
            Delete a policy
        """
        rvalue = self.client.hdel(self._hash, uid)
        if rvalue != 0:
            LOG.info('Deleted Policy with UID=%s.', uid)
