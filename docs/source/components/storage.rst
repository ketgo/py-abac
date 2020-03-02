Storage
=======

:class:`Storage` is a component which provides interface for implementing policy persistence. Thus it is used in
creating a :ref:`PAP <abac_pap>` with the exposed methods described in `Custom Backend`_ subsection. It is also used
by :ref:`components_pdp` to retrieve policies for evaluation. There can be various backend implementations like
RDBMS, NoSQL databases, etc. Py-ABAC ships with some out of the box:

.. toctree::

   MongoDB <backends/mongo>
   SQL <backends/sql>
   Memory <backends/memory>

Custom Backend
--------------

You can create your own policy storage by implementing :class:`Storage`. It exposes the following methods:

.. code-block:: python

   from py_abac.storage.base import Storage


   class MyStorage(Storage):
       """
           My custom backend specific storage
       """

       def add(policy):
           """
               Store a Policy
           """

       def get(uid):
           """
               Retrieve a Policy by its ID
           """

       def get_all(limit, offset):
           """
               Retrieve all stored Policies (with pagination)
           """

       def update(policy):
           """
               Store an updated Policy
           """

       def delete(uid):
           """
               Delete Policy from storage by its ID
           """

       def get_for_target(subject_id, resource_id, action_id):
           """
               Retrieve Policies that match the given target IDs
           """

The first 5 methods are used for creating a :ref:`PAP <abac_pap>` while the last method is used by :class:`PDP`.

.. important::

   Care must be taken when implementing :code:`get_for_target`. Incorrect filtering strategies in the method may lead
   to wrong access decisions by :class:`PDP`.

Migrations
----------

Migrations are a set of components that are useful for :class:`Storage` backends. The design and implementation is taken
from the `Vakt <https://github.com/kolotaev/vakt>`_ SDK. It's recommended in favor over manual actions on DB schema/data
since it's aware of Py-ABAC requirements. But it's not mandatory. It is up to a particular storage to decide whether it
needs migrations. It consists of 3 components:


* :class:`Migration`
* :class:`MigrationSet`
* :class:`Migrator`

:class:`Migration` allows you to describe data modifications between versions. Each storage can have a number of
:class:`Migration` classes to address different releases with the order of the migration specified in :code:`order`
property. The class should be located inside corresponding storage package and should implement
:class:`py_abac.storage.migration.Migration`. Migration has 2 main methods (as you might guess) and 1 property:

* :code:`up` - runs db "schema" upwards
* :code:`down` - runs db "schema" downwards (rolls back the actions of :code:`up`)
* :code:`order` - tells the number of the current migration in a row

:class:`MigrationSet` is a component that represents a collection of migrations for a storage. You should define your
own migration-set. It should be located inside corresponding storage package and should implement
:class:`py_abac.storage.migration.MigrationSet`. It has 3 methods that lest unimplemented:

* :code:`migrations` - should return all initialized :class:`Migration` objects
* :code:`save_applied_number` - saves a number of lst applied up migration in the storage for later reference
* :code:`last_applied` - returns a number of a lst applied up migration from the storage

:class:`Migrator` is an executor of migrations. It can execute all migrations up or down, or execute a particular
migration if :code:`number` argument is provided.

Example usage:

.. code-block:: python

   from pymongo import MongoClient
   from py_abac.storage.mongo import MongoStorage, MongoMigrationSet
   from py_abac.storage.migration import Migrator

   client = MongoClient('localhost', 27017)
   storage = MongoStorage(client, 'database-name', collection='optional-collection-name')

   migrator = Migrator(MongoMigrationSet(storage))
   migrator.up()
   ...
   migrator.down()
   ...
   migrator.up(number=2)
   ...
   migrator.down(number=2)
