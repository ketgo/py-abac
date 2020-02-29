.. _backend_sql:

SQL
^^^

SQL storage is backed by `SQLAlchemy <https://www.sqlalchemy.org/>`_, thus it should support any RDBMS available for it: MySQL, Postgres, Oracle, MSSQL,
Sqlite, etc.

Example for MySQL:

.. code-block:: python

   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker, scoped_session
   from py_abac.storage import SQLStorage, SQLMigrationSet
   from py_abac.storage.migration import Migrator

   # Creating SQL storage
   engine = create_engine('mysql://root:root@localhost/py_abac')
   storage = SQLStorage(scoped_session=scoped_session(sessionmaker(bind=engine)))

   # Running migrations
   migrator = Migrator(SQLMigrationSet(storage))
   migrator.up()

.. note::

   Currently py-abac focuses on testing functionality only for two most popular open-source databases: MySQL and Postgres.
   Other databases support may have worse performance characteristics and/or bugs. Feel free to report any issues.
