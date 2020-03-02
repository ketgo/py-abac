.. py-ABAC documentation master file, created by
   sphinx-quickstart on Wed Oct 16 11:13:25 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Py-ABAC's documentation!
===================================

.. image:: https://travis-ci.com/ketgo/py-abac.svg?token=oCVxhfjJAa2zDdszGjoy&branch=master
   :target: https://travis-ci.com/ketgo/py-abac
   :alt: Build Status


.. image:: https://codecov.io/gh/ketgo/pyabac/coverage.svg?branch=master
   :target: https://codecov.io/gh/ketgo/pyabac/coverage.svg?branch=master
   :alt: codecov.io


.. image:: https://img.shields.io/badge/License-Apache%202.0-yellow.svg
   :target: https://raw.githubusercontent.com/kolotaev/vakt/master/LICENSE
   :alt: Apache 2.0 licensed
..


Py-ABAC is an attribute-based access control (\ `ABAC <https://en.wikipedia.org/wiki/Attribute-based_access_control>`_\ )
toolkit based on policies. ABAC gives you a fine-grained control on definition of the rules that restrict an access to
resources and is generally considered a "next generation" authorization model. The design of py-ABAC stems from the
`XACML <https://en.wikipedia.org/wiki/XACML>`_ standard, and the ABAC python SDK `Vakt <https://github.com/kolotaev/vakt>`_.

See :ref:`concepts` for more detail.

Installation
------------

PyABAC runs on Python >= 3.5. PyPy implementation is supported as well.

To install run the following:

.. code-block:: bash

   pip install py-abac

Quick Example
-------------

The following code shows a quick example usage of Py-ABAC:

.. code-block:: python

   from pymongo import MongoClient
   from py_abac import PDP, Policy, Request
   from py_abac.storage import MongoStorage

   # Policy definition in JSON
   policy_json = {
       "uid": "1",
       "description": "Max and Nina are allowed to create, delete, get any "
                      "resources only if the client IP matches.",
       "effect": "allow",
       "rules": {
           "subject": [{"$.name": {"condition": "Equals", "value": "Max"}},
                       {"$.name": {"condition": "Equals", "value": "Nina"}}],
           "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
           "action": [{"$.method": {"condition": "Equals", "value": "create"}},
                      {"$.method": {"condition": "Equals", "value": "delete"}},
                      {"$.method": {"condition": "Equals", "value": "get"}}],
           "context": {"$.ip": {"condition": "CIDR", "value": "127.0.0.1/32"}}
       },
       "targets": {},
       "priority": 0
   }
   # Parse JSON and create policy object
   policy = Policy.from_json(policy_json)

   # Setup policy storage
   client = MongoClient()
   storage = MongoStorage(client)
   # Add policy to storage
   storage.add(policy)

   # Create policy decision point
   pdp = PDP(storage)

   # A sample access request JSON
   request_json = {
       "subject": {
           "id": "",
           "attributes": {"name": "Max"}
       },
       "resource": {
           "id": "",
           "attributes": {"name": "myrn:example.com:resource:123"}
       },
       "action": {
           "id": "",
           "attributes": {"method": "get"}
       },
       "context": {
           "ip": "127.0.0.1"
       }
   }
   # Parse JSON and create access request object
   request = Request.from_json(request_json)

   # Check if access request is allowed. Evaluates to True since
   # Max is allowed to get any resource when client IP matches.
   assert pdp.is_allowed(request)


Documentation
=============

.. toctree::
   :maxdepth: 3

   concepts
   components/components
   policy_language

.. toctree::
   :maxdepth: 1

   modules/modules

.. toctree::
   :maxdepth: 1

   license

Logging
-------

Py-ABAC follows a common logging pattern for libraries:

Its corresponding modules log all the events that happen but the log messages by default are handled by ``NullHandler``. It's up to the outer code/application to provide desired log handlers, filters, levels, etc.

For example:

.. code-block:: python

   import logging

   root = logging.getLogger()
   root.setLevel(logging.INFO)
   root.addHandler(logging.StreamHandler())

   ... # here go all the py_abac calls.

Acknowledgements
----------------

The conceptual and implementation design of Py-ABAC stems from the `XACML <https://en.wikipedia.org/wiki/XACML>`_
standard and the ABAC python SDK `Vakt <https://github.com/kolotaev/vakt>`_.

Development
-----------

To hack Py-ABAC locally run:

.. code-block:: bash

   $ pip install -e .[dev]         # to install all dependencies
   $ docker run --rm -d -p 27017:27017 mongo           # Run mongodb server on docker
   $ pytest --cov=py_abac tests/           # to get coverage report
   $ pylint py_abac            # to check code quality with PyLint
   $ bandit py_abac            # to check code security with Bandit

Optionally you can use ``make`` to perform development tasks.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
