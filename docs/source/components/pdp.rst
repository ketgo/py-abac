PDP
===

This component is the :ref:`policy decision point <abac_pdp>`, instantiated through the :class:`PDP` class. It is the
main entry point of py-abac for evaluating policies. At a minimum, a :ref:`Storage <components_storage>` object is required to
create a :class:`PDP` object. It has one method, :code:`is_allowed`, which when passed a :class:`AccessRequest`
object, gives you a boolean answer: is access allowed or not?

.. code-block:: python

   from pymongo import MongoClient
   from py_abac import PDP
   from py_abac.storage import MongoStorage

   # Setup storage
   client = MongoClient()
   st = MongoStorage(client)
   # Insert all polices to storage
   for p in policies:
       st.add(p)

   # Create PDP
   pdp = PDP(st)

   # Evaluate if access is allowed
   if pdp.is_allowed(request):
       return "Access Allowed", 200
   else:
       return "Unauthorized Access", 401

By default :class:`PDP`` uses the :class:`DenyOverrides` algorithm for policy evaluation. To specify otherwise, pass the
evaluation algorithm at creation. Moreover, a list of :class:`AttributeProvider` objects can also be provided. See the
sub-section :ref:`components_attribute_provider` for details of their usage.

.. code-block:: python

   from py_abac import PDP, EvaluationAlgorithm
   from py_abac.storage import MongoStorage
   from py_abac.providers import AttributeProvider

   # A simple email attribute provider class
   class EmailAttributeProvider(AttributeProvider):
       def get_attribute_value(self, ace, attribute_path, ctx):
           return "example@gmail.com"

   # Setup storage
   client = MongoClient()
   st = MongoStorage(client)
   # Insert all polices to storage
   for p in policies:
       st.add(p)

   # Create PDP configured to use highest priority algorithm
   # and an additional email attribute provider
   pdp = PDP(st, EvaluationAlgorithm.HIGHEST_PRIORITY, [EmailAttributeProvider()])

The three supported evaluation algorithms are:

- :class:`EvaluationAlgorithm.DENY_OVERRIDES`
- :class:`EvaluationAlgorithm.ALLOW_OVERRIDES`
- :class:`EvaluationAlgorithm.HIGHEST_PRIORITY`
