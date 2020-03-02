Access Request JSON
-------------------

An access request is a data object sent by :ref:`PEP <abac_pep>` to :ref:`PDP <abac_pdp>`. This object contains all the
information needed by the PDP to evaluate the policies and return access decision. The JSON schema of the object is
given by:

.. code-block::

   {
       "subject": {
           "id": <string>,
           "attributes": <attribute_block>
       },
       "resource": {
           "id": <string>,
           "attributes": <attribute_block>
       },
       "action": {
           "id": <string>,
           "attributes": <attribute_block>
       },
       "context": <attribute_block>
   }

where :code:`<attribute_block>` is just a JSON block containing one or more attribute-value pairs. An example request is
shown below:

.. code-block:: json

   {
       "subject": {
         "id": "a",
         "attributes": {
           "firstName": "Carl",
           "lastName": "Right"
         }
       },
       "resource": {
         "id": "a",
         "attributes": {
           "name": "Calendar"
         }
       },
       "action": {
         "id": "",
         "attributes": {}
       },
       "context": {}
   }
