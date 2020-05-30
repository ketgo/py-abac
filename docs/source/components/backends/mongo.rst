.. _backend_mongo:

MongoDB
^^^^^^^

MongoDB is chosen as the most popular and widespread NO-SQL database.

.. code-block:: python

   from pymongo import MongoClient
   from py_abac.storage import MongoStorage

   client = MongoClient('localhost', 27017)
   storage = MongoStorage(client, 'database-name', collection='optional-collection-name')

Default database and collection names are 'py_abac' and  'py_abac_policies' respectively.

All standard :class:`PAP` operations as defined in the interface ``py_abac.storage.base.StorageBase`` are supported.
