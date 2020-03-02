Targets Block
~~~~~~~~~~~~~

The targets block specifies for which instances of access control elements a policy applies. This block contains one or
more 'ID' attribute values for :code:`subject`, :code:`resource`, and :code:`action` fields. Thus in Py-ABAC it is
mandatory that these three access control elements have a string valued ID attribute in the :class:`AccessRequest` object.
The JSON schema for the block is given by:

.. code-block::

   {
       "subject_id": ["<id_string>", "<id_string>", ... ],
       "resource_id": ["<id_string>", "<id_string>", ... ],
       "action_id": ["<id_string>", "<id_string>", ... ]
   }

where  :code:`"<id_string>"` denotes string values of the ‘ID’ attribute. The array here acts as an implicit OR operator.
Furthermore wild-carded values for :code:`"<id_string>"` are also supported:

.. code-block:: json

   {
       "subject_id": ["a", "b"],
       "resource_id": ["ab*"],
       "action_id": ["*"]
   }

This example states that the policy is only applicable when the subject ID is either set to “a” or “b”, and when the
resource ID starts with “ab”. The action can have any ID value.

For convince, the array can be omitted when only a single :code:`"<id_string>"` is to be set. Thus the above target
block can also be defined as:

.. code-block:: json

   {
       "subject_id": ["a", "b"],
       "resource_id": "ab*",
       "action_id": "*"
   }

.. note::

   When no target block is explicitly specified, the policy is considered to be applicable for all targets as Py-ABAC
   uses the following default:

   .. code-block:: json

      {
          "subject_id": "*",
          "resource_id": "*",
          "action_id": "*"
      }
