.. _policy_language:

Policy Language
===============

This section presents the JSON-based policy language for Py-ABAC. There are two subsections. The first subsection discusses JSON structure of a policy, while the latter about the access request.

Policy JSON
-----------

A policy composes of :code:`uid`, :code:`description`, :code:`conditions` , :code:`targets`, :code:`effect`,
and :code:`priority` fields. The JSON schema is given by

.. code-block::

   {
       "uid": <string>,
       "description": <string>,
       "rules": <rules_block>,
       "targets": <targets_block>,
       "effect": <string>,
       "priority": <number>
   }

where :code:`<rules_block>` and :code:`<targets_block>` are JSON blocks discussed in detail in the :ref:`rules_block`
and :ref:`targets_block` sections. Essentially, the :code:`"targets"` and :code:`"rules"` fields are used to define
conditions on the attributes of access control elements. When these conditions are satisfied, the policy applies and
the value for the :code:`"effect"` field is returned by the :class:`PDP`. Thus :code:`"effect"` is the returned decision
of the policy and can be either :code:`"allow"` or :code:`"deny"`. The  :code:`"uid"` field is a string value that
uniquely identifies a policy. As the name suggests, the :code:`"description"` field stores description of the policy.
Finally, :code:`"priority"` provides a numeric value indicating the weight of the policy when its decision conflicts
with other policy under the :class:`HighestPriority` evaluation algorithm. By default this field is set to :code:`0` for
all policies.

Targets vs Rules
~~~~~~~~~~~~~~~~

The concept of code:`"targets"` and :code:`"rules"` in Py-ABAC is derived from the XACML standard. Both are used to
define conditions on attributes during policy creation. There is however a fundamental distinction between the two which
will become more clear in the following sections. From a conceptual standpoint, :code:`"targets"` states for which
instances of access control elements a policy applies. Thus called targets of a policy. The :code:`"rules"` on the
other-hand define conditions on the attributes of the targets. To illustrate this point, lets consider a system with two
users, "Sam" and "John". Each user has an attribute called "age". Suppose we want to create a policy where "Sam" can
access the system only if he is above 18 years old. To achieve this we take "Sam" and "John" as instances of the subject
access control element. We then set the subject target of the policy to "Sam" while the rule to the condition "age" > 18.
The exact syntax to do so is shown in the following sections.

.. note::

   Similar to XACML implementations, Py-ABAC also retrieve policies from a persistent storage filtering on target IDs.
   This results in efficient lookup, reducing the burden of :class:`PDP` evaluating all policies in the storage.

.. _targets_block:

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

.. _rules_block:

Rules Block
~~~~~~~~~~~

Rules are boolean expressions defined on the attributes of the targeted instances of access control elements. The JSON
schema is given by

.. code-block::

   {
       "subject": <boolean_expression>,
       "resource": <boolean_expression>,
       "action": <boolean_expression>,
       "context": <boolean_expression>
   }

with :code:`<boolean_expression>` being a JSON block for boolean expression.

A policy is considered applicable only when each of the boolean expressions are satisfied. These expressions define
constraints on the attribute values of the access control elements. The constraints can be as simple as those involving
only a single attribute, or can be complex involving multiple attributes. A simple Boolean expression consists of a
key-value pair as shown below:

.. code-block::

   {<attribute_path>: <condition_expression>}

The key specifies the attribute in `ObjectPath <http://objectpath.org/>`_ notation while the value is a conditional
expression. Use of the `ObjectPath <http://objectpath.org/>`_ notation gives Py-ABAC the powerful ability to define
conditions on nested attributes. The :code:`<condition_expression>` is again a JSON block specifying the requirements
that the attribute value needs to meet. Different supported condition expressions are shown in :ref:`conditions_blocks`
section. As an example, the condition block for the requirement that “firstName” sub-attribute of “name” in the subject
access control element should be "Max" is shown below:

.. code-block:: json

   {
       "subject": {
           "$.name.firstName": {
               "condition": "Eq",
               "value": "Max"
           }
       }
   }

Sometimes conditions on a single attribute does not suffice and constraints on multiple attributes connected by logical
relations like AND or OR are required. In Py-ABAC this is achieved by using in-built *object* and *array* JSON data
structures as implicit logical operators. An *object* is implicitly an AND operator which would be evaluated to true
only if all the included key-value pairs are evaluated to true. Similarly, an *array* is implicitly an OR operator which
would be evaluated to true as long as at least one of its members is evaluated to true. For an example see the following
conditional blocks:

.. code-block:: json

   {
       "subject": {
           "$.name.firstName": {
               "condition": "Eq",
               "value": "Carl"
           },
           "$.name.lastName": {
               "condition": "Eq",
               "value": "Rubin"
           },
       },
       "resource": [
           {
               "$.name": {
                   "condition": "Eq",
                   "value": "Default"
               }
           },
           {
               "$.type": {
                   "condition": "Eq",
                   "value": "Book"
               }
           }
       ]
   }

Overall the rule states that the subject should have “firstName” valued “Carl” AND “lastName” valued “Rubin”. Similarly,
the resource should have a “name” attribute valued “Default” OR “type” valued “Book”.

.. _conditions_blocks:

Condition Blocks
~~~~~~~~~~~~~~~~

There are basically six types of :code:`<condition_expression>` blocks supported in Py-ABAC:

- :ref:`Numeric <numeric_conditions>`
- :ref:`String <string_conditions>`
- :ref:`Collection <collection_conditions>`
- :ref:`Object <object_conditions>`
- :ref:`Logic <logic_conditions>`
- :ref:`Other <other_conditions>`

The JSON schema and examples for each are shown in the following tables.

.. _numeric_conditions:

Numeric Condition Block
^^^^^^^^^^^^^^^^^^^^^^^

**JSON Schema:**

.. code-block::

   {
     "condition": <string>,
     "value": <number>
   }

+---------------------+---------------------------------------------------------------------------------+
| **Field**           | **Description**                                                                 |
+---------------------+---------------------------------------------------------------------------------+
| :code:`"condition"` | Specifies the type of numeric condition. Possible values are:                   |
|                     |                                                                                 |
|                     | - :code:`Eq`: attribute value equals that in :code:`"value"`                    |
|                     | - :code:`Neq`: attribute value not equals that in :code:`"value"`               |
|                     | - :code:`Gt`: attribute value is greater than that in :code:`"value"`           |
|                     | - :code:`Gte`: attribute value is greater than equal to that in :code:`"value"` |
|                     | - :code:`Lt`: attribute value is less than that in :code:`"value"`              |
|                     | - :code:`Lte`: attribute value is less than equal to that in :code:`"value"`    |
+---------------------+---------------------------------------------------------------------------------+
| :code:`"value"`     | Contains a number. This can be a float or an integer.                           |
+---------------------+---------------------------------------------------------------------------------+

**Example:**

.. code-block:: json

   {
     "condition": "Lte",
     "value": 1.5
   }

.. _string_conditions:

String Condition Block
^^^^^^^^^^^^^^^^^^^^^^

**JSON Schema:**

.. code-block::

   {
     "condition": <string>,
     "value": <string>,
     "case_insensitive": <bool>
   }

+----------------------------+-----------------------------------------------------------------------------------------+
| Field                      | Description                                                                             |
+----------------------------+-----------------------------------------------------------------------------------------+
| :code:`"condition"`        | Specifies the type of string condition. Possible values are:                            |
|                            |                                                                                         |
|                            | - :code:`"Equals"`: attribute value string equals that in :code:`"value"`               |
|                            | - :code:`"NotEquals"`: attribute value string not equals that in :code:`"value"`        |
|                            | - :code:`"Contains"`: attribute value contains the string in :code:`"value"`            |
|                            | - :code:`"NotContains"`: attribute value does not contain the string in :code:`"value"` |
|                            | - :code:`"StartsWith"`: attribute value starts with string in :code:`"value"`           |
|                            | - :code:`"EndsWith"`: attribute value ends with string in :code:`"value"`               |
|                            | - :code:`"RegexMatch"`: attribute value string matches regex pattern in :code:`"value"` |
+----------------------------+-----------------------------------------------------------------------------------------+
| :code:`"value"`            | Contains a basic string or regex pattern.                                               |
+----------------------------+-----------------------------------------------------------------------------------------+
| :code:`"case_insensitive"` | String case insensitive condition flag.                                                 |
|                            | This is an optional field and by default is set to :code:`False`.                       |
+----------------------------+-----------------------------------------------------------------------------------------+

**Example:**

.. code-block:: json

   {
     "condition": "StartsWith",
     "value": "Cal"
   }

.. _collection_conditions:

Collection Condition Block
^^^^^^^^^^^^^^^^^^^^^^^^^^

#.  **JSON Schema:**

    .. code-block::

       {
         "condition": <string>,
         "values": <list>
       }

    +---------------------+-----------------------------------------------------------------------------------------------------------------+
    | Field               | Description                                                                                                     |
    +---------------------+-----------------------------------------------------------------------------------------------------------------+
    | :code:`"condition"` | Specifies the type of collection condition. Possible values are:                                                |
    |                     |                                                                                                                 |
    |                     | - :code:`"AllIn"`: all members of attribute value collection are members of :code:`"values"`                    |
    |                     | - :code:`"AllNotIn"`: none of the members of attribute value collection are members of :code:`"values"`         |
    |                     | - :code:`"AnyIn"`: one or more members of the attribute value collection are members of :code:`"values"`        |
    |                     | - :code:`"AnyNotIn"`: one or more members of the attribute value collection are not members of :code:`"values"` |
    |                     | - :code:`"IsIn"`: attribute value (treated as a single value) is member of :code:`"values"`                     |
    |                     | - :code:`"IsNotIn"`: attribute value (treated as a single value) is not member of :code:`"values"`              |
    +---------------------+-----------------------------------------------------------------------------------------------------------------+
    | :code:`"value"`     | Collection of primitive type values like string, int ,float, etc.                                               |
    +---------------------+-----------------------------------------------------------------------------------------------------------------+

    **Example:**

    .. code-block:: json

       {
         "condition": "AnyIn",
         "values": ["Example1", "Example2"]
       }

#.  **JSON Schema:**

    .. code-block::

       {
         "condition": <string>
       }

    +---------------------+-------------------------------------------------------------------+
    | Field               | Description                                                       |
    +---------------------+-------------------------------------------------------------------+
    | :code:`"condition"` | Specifies the type of collection condition. Possible values are:  |
    |                     |                                                                   |
    |                     | - :code:`"IsEmpty"`: attribute value collection is empty          |
    |                     | - :code:`"IsNotEmpty"`: attribute value collection is not empty   |
    +---------------------+-------------------------------------------------------------------+

    **Example:**

    .. code-block:: json

       {
         "condition": "IsEmpty"
       }

.. _object_conditions:

Object Condition Block
^^^^^^^^^^^^^^^^^^^^^^

**JSON Schema:**

.. code-block::

   {
     "condition": "EqualsObject",
     "value": <object>
   }

+---------------------+--------------------------------------------------------------------------------------+
| Field               | Description                                                                          |
+---------------------+--------------------------------------------------------------------------------------+
| :code:`"condition"` | Specifies the type of object condition. Possible values are:                         |
|                     |                                                                                      |
|                     | - :code:`"EqualsObject"`: attribute value JSON object equals that in :code:`"value"` |
+---------------------+--------------------------------------------------------------------------------------+
| :code:`"value"`     | Contains a JSON object                                                               |
+---------------------+--------------------------------------------------------------------------------------+

**Example:**

.. code-block:: json

   {
     "condition": "EqualsObject",
     "value": {"name": "Sam"}
   }

.. _logic_conditions:

Logic Condition Block
^^^^^^^^^^^^^^^^^^^^^

#.   **JSON Schema:**

    .. code-block::

       {
         "condition": <string>,
         "values": <list<condition_expression>>
       }

    +---------------------+----------------------------------------------------------------------------------------+
    | Field               | Description                                                                            |
    +---------------------+----------------------------------------------------------------------------------------+
    | :code:`"condition"` | Specifies the type of logic condition. Possible values are:                            |
    |                     |                                                                                        |
    |                     | - :code:`"AnyOf"`: attribute value satisfies any of the conditions in :code:`"values"` |
    |                     | - :code:`"AllOf"`: attribute value satisfies all of the conditions in :code:`"values"` |
    +---------------------+----------------------------------------------------------------------------------------+
    | :code:`"value"`     | Contains a list of :code:`<condition_expression>` blocks.                              |
    +---------------------+----------------------------------------------------------------------------------------+

    **Example:**

    .. code-block:: json

       {
         "condition": "AllOf",
         "values": [
             {"condition": "Lt", "value": 1.5},
             {"condition": "Gt", "value": 0.5}
           ]
       }

#.   **JSON Schema:**

    .. code-block::

       {
         "condition": "Not",
         "value": <condition_expression>
       }

    +---------------------+------------------------------------------------------------------------------------+
    | Field               | Description                                                                        |
    +---------------------+------------------------------------------------------------------------------------+
    | :code:`"condition"` | Specifies the type of logic condition. Possible values are:                        |
    |                     |                                                                                    |
    |                     | - :code:`"Not"`: attribute value does not satisfy the condition in :code:`"value"` |
    +---------------------+------------------------------------------------------------------------------------+
    | :code:`"value"`     | Contains a :code:`<condition_expression>` block.                                   |
    +---------------------+------------------------------------------------------------------------------------+

    **Example:**

    .. code-block:: json

       {
           "condition": "Not",
           "value": {"condition": "Eq", "value": 1.5}
       }

.. _other_conditions:

Other Condition Block
^^^^^^^^^^^^^^^^^^^^^

#.   **JSON Schema:** :code:`"CIDR"`

    .. code-block::

       {
         "condition": "CIDR",
         "value": <string>
       }

    +---------------------+---------------------------------------------------------------------------------------------+
    | Field               | Description                                                                                 |
    +---------------------+---------------------------------------------------------------------------------------------+
    | :code:`"condition"` | Specifies the :code:`"CIDR"` network condition:                                             |
    |                     |                                                                                             |
    |                     | - :code:`"CIDR"`: IP address in attribute value is within the CIDR block in :code:`"value"` |
    +---------------------+---------------------------------------------------------------------------------------------+
    | :code:`"value"`     | Contains a CIDR block as string.                                                            |
    +---------------------+---------------------------------------------------------------------------------------------+

    **Example:**

    .. code-block:: json

       {
           "condition": "CIDR",
           "value": "10.0.0.0/16"
       }

#.   **JSON Schema:** :code:`"EqualsAttribute"`

    .. code-block::

       {
         "condition": "EqualsAttribute",
         "ace": <string>,
         "path": <string>
       }

    +---------------------+--------------------------------------------------------------------------------------------------------+
    | Field               | Description                                                                                            |
    +---------------------+--------------------------------------------------------------------------------------------------------+
    | :code:`"condition"` | Specifies the :code:`"EqualsAttribute"` condition:                                                     |
    |                     |                                                                                                        |
    |                     | - :code:`"EqualsAttribute"`: attribute value equals the value of attribute at location :code:`"path"`  |
    |                     |   of :code:`"ace"` access control element                                                              |
    +---------------------+--------------------------------------------------------------------------------------------------------+
    | :code:`"ace"`       | Specifies access control element. The value for this field should be either :code:`"subject"`,         |
    |                     | :code:`"resource"`, :code:`"action"`, or :code:`"context"`                                             |
    +---------------------+--------------------------------------------------------------------------------------------------------+
    | :code:`"path"`      | Specified the attribute path in ObjectPath notation of the access control element in :code:`"ace"`     |
    +---------------------+--------------------------------------------------------------------------------------------------------+

    **Example:**

    .. code-block:: json

       {
           "condtion": "EqualsAttribute",
           "ace": "context",
           "path": "$.network.name"
       }

#.   **JSON Schema:** :code:`"Any"`, :code:`"Exists"`, :code:`"NotExists"`

    .. code-block::

         {
           "condition": <string>
         }

    +---------------------+-----------------------------------------------------------------------+
    | Field               | Description                                                           |
    +---------------------+-----------------------------------------------------------------------+
    | :code:`"condition"` | Specifies the type of condition:                                      |
    |                     |                                                                       |
    |                     | - :code:`"Any"`: attribute contains any value, null value included    |
    |                     | - :code:`"Exists"`: attribute exists by checking if it's not null     |
    |                     | - :code:`"NotExists"`: attribute does not exits by checking it's null |
    +---------------------+-----------------------------------------------------------------------+

    **Example:**

    .. code-block:: json

       {
           "condition": "Any"
       }

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
