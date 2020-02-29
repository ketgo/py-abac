AttributeProvider
=================

:class:`AttributeProvider` is an interface to create a :ref:`PIP <abac_pip>`. The purpose of this object is to provide
attribute values missing in the :class:`AccessRequest` object. During policy evaluation, the :class:`PDP` first checks
the :class:`Request` object for attribute values; If no values are found, it then checks the list of
:class:`AttributeProvider` objects passed during :class:`PDP` creation. In order to create an :class:`AttributeProvider`
object, you need to implement the :code:`get_attribute_value` method:

.. code-block:: python

   from py_abac.provider.base import AttributeProvider

   # A simple email attribute provider class
   class EmailAttributeProvider(AttributeProvider):
       def get_attribute_value(self, ace, attribute_path, ctx):
           """
               Returns a value for an attribute. If value not found
               then return None.


               :param ace: string value indicating the access control
                           element, i.e. "subject", "resource", "action"
                           or "context".
               :param attribute_path: string in ObjectPat notation indicating
                                      the attribute for which the value is
                                      requested.
               :param ctx: evaluation context
           """
           return "example@gmail.com"

As seen in the above example, :code:`get_attribute_value` takes in three arguments: :code:`ace`, :code:`attribute_path`
and :code:`ctx`. The :code:`ace` is a string value indicating for which access control element the attribute value is
being requested. This argument will be set to either :code:`"subject"`, :code:`"resource"`, :code:`"action"`, or
:code:`"context"``. The :code:`attribute_path` argument is a string in  `ObjectPath <http://objectpath.org/>`_ notation
denoting the attribute for which the value is being requested. The :code:`ctx` argument is an :ref:`components_evaluation_context`
object. The primary purpose of this argument is to retrieve values of other attributes. Thus a common use-case would be
to return values conditioned upon other attributes:

.. code-block:: python

   # An email attribute provider class
   class EmailAttributeProvider(AttributeProvider):
       def get_attribute_value(self, ace, attribute_path, ctx):
           # Return email for Max
           if ctx.get_attribute_value("subject", "$.name") == "Max":
               return "max@gmail.com"
           # Else return default email
           return "default@gmail.com"

.. important::

   If the :class:`AttributeProvider` does not contain value for an attribute, the :code:`get_attribute_value` must
   return :code:`None`.

