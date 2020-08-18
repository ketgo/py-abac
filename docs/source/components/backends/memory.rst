.. _backend_memory:

In-Memory
^^^^^^^^^

The In-Memory backend stores the policies in RAM and is the default storage used. The usage is as shown below:

.. code-block:: python

   from py_abac.storage.memory import MemoryStorage

   # In-Memory storage
   storage = MemoryStorage()

   # Retrieve policy with UID 1
   policy = storage.get("1")

.. important::

    Currently the In-Memory storage returns all policies for evaluation by PDP. In the future indexing
    will be added for filtering of policies to improve lookup efficiency.

.. important::

    It should be noted that the In-Memory backend does not persist policies and thus there is a risk of
    losing all policies on system restarts.
