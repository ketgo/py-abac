.. _backend_redis:

Redis
^^^^^

The Redis backend stores policies on a Redis server. The usage is as shown below:

.. code-block:: python

   from redis import Redis
   from py_abac.storage.redis import RedisStorage

   # Setup Redis client
   client = Redis('localhost', 6379)
   # Setup Redis storage. The storage is setup to store policies under hash "my_policies" on redis.
   storage = RedisStorage(client, hash_key="my_policies")

   # Retrieve policy with UID 1
   policy = storage.get("1")

Default hash key used by the storage is "py_abac_policies".

.. important::

    Currently the redis storage returns all policies for evaluation by PDP. There is no support
    for in-database filtering of policies yet.

.. note::

    Redis doesn't guarantee the exact number of elements returned on HSCAN operation. The storage
    thus gets all policies from Redis for the :method:`RedisStorage.get_all` method and manually
    slices the list according to the requested offset and limit.
