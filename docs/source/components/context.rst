EvaluationContext
=================

An :class:`EvaluationContext` object is created by the :class:`PDP` during policy evaluation. This object is used by
:class:`PDP` for retrieval of those attribute values referred by a policy. It has following properties:

.. code-block:: python

   # The target ID for subject access control element
   ctx.subject_id

   # The target ID for resource access control element
   ctx.resource_id

   # The target ID for action access control element
   ctx.action_id

   # Lookup a value for an attribute of an access control element
   ctx.get_attribute_value(ace: str, attribute_path: str)

During retrieval,  the :class:`EvaluationContext` first checks for an attribute value in the :class:`AccessRequest` object.
If the value is not found, it then checks all the :class:`AttributeProvider` objects sequentially.

.. note::

   As attribute values are retried from :class:`AttributeProvider` objects sequentially, an eager lookup is performed.
   This means any subsequent :class:`AttributeProvider` objects will be skipped moment the very first provider returns
   a value.
