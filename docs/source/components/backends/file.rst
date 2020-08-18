.. _backend_file:

File
^^^^

The file based backend stores the policies on disk is one or more files. The usage is as shown below:

.. code-block:: python

   from py_abac.storage.file import FileStorage

   # File storage reading and writing policies in specified directory
   storage = FileStorage("/data/policies")

   # Retrieve policy with UID 1
   policy = storage.get("1")

The policies are stored in a file called "policies" under the specified directory. As the file storage
uses the `shelve <https://docs.python.org/3/library/shelve.html>`_ package underneath, the files name
maybe get with prefixes.

.. important::

            This storage does not yet perform ACID transactions. It uses
            the python shelve package for storage which does not support
            transaction based access to stored objects. Thus so not use it
            in distributed applications. There is a separate project under
            development to address this issue.
