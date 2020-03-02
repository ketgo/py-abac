Policy
======

This is the component containing rules for accessing resources. A policy object can be created by first defining a
policy JSON using the JSON-based :ref:`policy_language`, and then parsing it using the :class:`Policy` class.

.. code-block:: python

   from py_abac import Policy

   # Policy definition in JSON-based policy language
   policy_json = {
       "uid": "1",
       "description": "Max is not allowed to create, delete, get any resource",
       "effect": "deny",
       "rules": {
           "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
           "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
           "action": [{"$.method": {"condition": "Equals", "value": "create"}},
                      {"$.method": {"condition": "Equals", "value": "delete"}},
                      {"$.method": {"condition": "Equals", "value": "get"}}],
           "context": {}
       },
       "targets": {},
       "priority": 0
   }
   # Prase policy JSON to create Policy object
   policy = Policy.from_json(policy_json)

See the :ref:`policy_language` section for detailed description of JSON structure.
