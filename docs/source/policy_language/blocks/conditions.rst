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
