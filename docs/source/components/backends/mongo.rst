.. _backend_mongo:

MongoDB
^^^^^^^

MongoDB is chosen as the most popular and widespread NO-SQL database.

.. code-block:: python

   from pymongo import MongoClient
   from py_abac.storage import MongoStorage, MongoMigrationSet
   from py_abac.storage.migration import Migrator

   client = MongoClient('localhost', 27017)
   storage = MongoStorage(client, 'database-name', collection='optional-collection-name')

   # Running migrations
   migrator = Migrator(SQLMigrationSet(storage))
   migrator.up()

Default database and collection names are 'py_abac' and  'py_abac_policies' respectively.

All standard :class:`PAP` operations as defined in the interface ``py_abac.storage.base.StorageBase`` are supported.
