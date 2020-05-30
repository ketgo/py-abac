.. _backend_memory:

In-Memory
^^^^^^

The In-Memory backend stores the policies in RAM and is the default storage used. Hence there is no need of explicitly
creating this backend. However, if you really like to do so, the bacend an be created as shown below:

.. code-block:: python

   from py_abac.storage import MemoryStorage

   # In-Memory storage
   storage = MongoStorage()

.. important::

    It should be noted that the In-Memory backend does not persist policies and thus there is a risk of losing all
    policies on system restarts.
