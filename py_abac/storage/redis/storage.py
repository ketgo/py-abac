"""
    Redis policy storage
"""

import json
import logging
from itertools import islice
from typing import Generator, Union

from redis import Redis

from ..base import Storage
from ...exceptions import PolicyExistsError
from ...policy import Policy

LOG = logging.getLogger(__name__)

DEFAULT_HASH_KEY = "py_abac_policies"


class RedisStorage(Storage):
    """
        Redis policy storage backend.

        :param client: redis client.
        :param hash_key: hash key under which policies are
            stored in database.
    """

    def __init__(self, client: Redis, hash_key: str = None):
        self.client = client
        self._hash = hash_key or DEFAULT_HASH_KEY

    def add(self, policy: Policy):
        """
            Store a policy
        """
        rvalue = self.client.hsetnx(self._hash, policy.uid, self.__to_policy_str(policy))
        if rvalue == 0:
            LOG.error('Error trying to create already existing policy with UID=%s.', policy.uid)
            raise PolicyExistsError(policy.uid)
        LOG.info('Added Policy: %s', policy)

    def get(self, uid: str) -> Union[Policy, None]:
        """
            Get specific policy
        """
        policy_str = self.client.hget(self._hash, uid)
        if not policy_str:
            return None
        return self.__to_policy(policy_str)

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        """
            Retrieve all the policies within a window

            .. note:

                Redis doesn't guarantee the exact number of elements returned
                thus this method gets all policies from Redis and manually
                slices the list.
        """
        self._check_limit_and_offset(limit, offset)
        rvalue = self.client.hgetall(self._hash)
        policies = islice(rvalue.values(), offset, offset + limit)
        for policy_str in policies:
            yield self.__to_policy(policy_str)

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        """
            Get all policies for given target IDs.

            .. note:

                Currently all policies are returned for evaluation by PDP.
        """
        # TODO: Create topologically sorted graph index for filtered retrieval.
        rvalue = self.client.hgetall(self._hash)
        for uid in rvalue:
            policy_str = rvalue[uid]
            yield self.__to_policy(policy_str)

    def update(self, policy: Policy):
        """
            Update a policy

            NOTE: The lua script is used to make sure an update
                operation occurs instead of upsert.
        """
        uid = policy.uid
        lua = \
            """
                if redis.call('HEXISTS', KEYS[1], ARGV[1]) == 1 then
                    return redis.call('HSET', KEYS[1], ARGV[1], ARGV[2])
                end
            """
        update_policy = self.client.register_script(lua)
        rvalue = update_policy(keys=[self._hash], args=[uid, self.__to_policy_str(policy)])
        if rvalue is not None:
            LOG.info('Updated Policy with UID=%s. New value is: %s', uid, policy)

    def delete(self, uid: str):
        """
            Delete a policy
        """
        rvalue = self.client.hdel(self._hash, uid)
        if rvalue != 0:
            LOG.info('Deleted Policy with UID=%s.', uid)

    @staticmethod
    def __to_policy(policy_str: bytes) -> Policy:
        """
            Converts stored policy string to policy object.
        """
        policy_json = json.loads(policy_str.decode("utf-8"))
        return Policy.from_json(policy_json)

    @staticmethod
    def __to_policy_str(policy: Policy) -> str:
        """
            Converts policy object to string for storage on Redis.
        """
        policy_json = policy.to_json()
        return json.dumps(policy_json)
