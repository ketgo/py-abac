.. _backend_memory:

In-Memory
^^^^^^

The In-Memory backend stores the policies in RAM and is the default storage used. The usage is as shown below:

.. code-block:: python

   from py_abac.storage import MemoryStorage

   # In-Memory storage
   storage = MemoryStorage()

   # Retrieve policy with UID 1
   policy = storage.get("1")

.. important::

    It should be noted that the In-Memory backend does not persist policies and thus there is a risk of losing all
    policies on system restarts.
