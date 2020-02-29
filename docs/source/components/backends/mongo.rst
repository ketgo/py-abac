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

Actions are the same as for any Storage that conforms interface of ``py_abac.storage.base.StorageBase`` base class.
