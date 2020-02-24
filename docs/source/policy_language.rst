Policy Language
===============

This section presents the JSON-based policy language for py-ABAC. There are two subsections. The first subsection discusses JSON structure of a policy, while the latter about the access request.

Policy JSON
-----------

A policy structure consists of ``uid``\ , ``description``\ , ``conditions``\ , ``targets``\ , ``effect``\ , and ``priority`` fields. The JSON schema is given by

.. code-block::

   {
       "uid": <string>,
       "description": <string>,
       "rules": <rules_block>,
       "targets": <targets_block>,
       "effect": <string>,
       "priority": <number>
   }

where ``<rules_block>`` and ``<targets_block>`` are JSON blocks discussed in detail in the `Rules Block <#rules-block>`_ and `Targets Block <#targets-block>`_ subsections. Essentially, the ``"targets"`` and ``"rules"`` fields are used to define conditions on the attributes of access control elements. When these conditions are satisfied, the policy applies and the value for the ``"effect"`` field is returned by the ``PDP``. Thus ``"effect"`` is the returned decision of the policy and can be either ``"allow"`` or ``"deny"``. The  ``"uid"`` field is a string value that uniquely identifies a policy. As the name suggests, the ``"description"`` field stores description of the policy. Finally, ``"priority"`` provides a numeric value indicating the weight of the policy when its decision conflicts with other policy under the ``HighestPriority`` evaluation algorithm. By default, this field is set to ``0`` for all policies.

Targets vs Rules
~~~~~~~~~~~~~~~~

The concept of ``"targets"`` and ``"rules"`` in py-ABAC is derived from the XACML standard. Both are used to define conditions on attributes during policy creation. There is however a basic distinction between the two. This distinction will become more clear in the following sections. From a conceptual standpoint, ``"targets"`` states for which access control elements a policy applies. In other words, targets of a policy. The ``"rules"`` on the other-hand define the conditions on the attributes of the targets. To illustrate this point, lets consider a system with two users, "Sam" and "John". Each user has an attribute called "age".  Suppose we want to create a policy where "Sam" can access the system only if he is above 18 years old. To achieve this, we set the target of the policy to "Sam" while the rule to the condition "age" > 18. The exact syntax to do so is shown in the following sections.

Targets Block
~~~~~~~~~~~~~

The targets block specifies for which access control elements a policy applies. This block contains one or more 'ID' attribute values for ``subject``\ , ``resource``\ , and ``action`` fields. Thus in py-ABAC it is mandatory that these three access control elements have a string valued ID attribute in the ``Request`` object. The JSON schema for the block is

.. code-block::

   {
       "subject_id": ["<id_string>", "<id_string>", ... ],
       "resource_id": ["<id_string>", "<id_string>", ... ],
       "action_id": ["<id_string>", "<id_string>", ... ]
   }

where  ``<id_string>`` denotes string values of the ‘ID’ attribute. The array here acts as an implicit OR operator. Furthermore wild-carded values for ``<id_string>`` are also supported:

.. code-block:: json

   {
       "subject_id": ["a", "b"],
       "resource_id": ["ab*"],
       "action_id": ["*"]
   }

This example states that the policy is only applicable when the subject ID is either set to “a” or “b”, and when the resource ID starts with “ab”. The action can have any ID value.

For convince, the array can be omitted when only a single ``<id_string>`` is to be set for a filed. Thus the above target block can also be defined as

.. code-block:: json

   {
       "subject_id": ["a", "b"],
       "resource_id": "ab*",
       "action_id": "*"
   }

Note that when no target block is explicitly specified, the policy is considered to be applicable for all targets as py-ABAC uses the following default:

.. code-block:: json

   {
       "subject_id": "*",
       "resource_id": "*",
       "action_id": "*"
   }

Rules Block
~~~~~~~~~~~

Rules are Boolean expressions defined on the attributes of the targeted access control elements. The JSON schema is given by

.. code-block:: json

   {
       "subject": "<boolean_expression>",
       "resource": "<boolean_expression>",
       "action": "<boolean_expression>",
       "context": "<boolean_expression>"
   }

with ``<boolean_expression>`` being a JSON block for Boolean expression.

A policy is considered applicable only when each of the Boolean expressions are satisfied. These expressions define constraints on the attribute values of the access control elements. The constraints can be as simple as those involving only a single attribute, or can be complex involving multiple attributes. A simple Boolean expression consists of a key-value pair as shown below:

.. code-block:: json

   {"<attribute_path>": "<condition_expression>"}

The key specifies the attribute in `ObjectPath <http://objectpath.org/>`_ notation while the value is a conditional expression. Use of the `ObjectPath <http://objectpath.org/>`_ notation gives py-ABAC the powerful ability to define conditions on nested attributes. The ``<condition_expression>`` is again a JSON block specifying the requirements that the attribute value needs to meet. Different supported condition expressions are shown in `Condition Blocks <#condition-blocks>`_ subsection. As an example, the condition block for the requirement that “firstName” sub-attribute of “name” attribute of the subject field should be "Max" is shown below:

.. code-block:: json

   {
       "subject": {
           "$.name.firstName": {
               "condition": "Eq",
               "value": "Max"
           }
       }
   }

Sometimes conditions on a single attribute does not suffice and constraints on multiple attributes connected by logical relations like AND or OR are required. In py-ABAC, this is achieved by using in-built JSON data structures *object* and *array* as implicit logical operators. An *object* is implicitly an AND operator which would be evaluated to true only if all the included key-value pairs are evaluated to true. Similarly, an *array* is implicitly an OR operator which would be evaluated to true as long as at least one of its members is evaluated to true. For an example see the following conditional blocks:

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

The overall rule states that the subject should have the “firstName” sub-attribute valued “Carl”, AND “lastName” sub-attribute valued “Rubin”. Similarly, the resource should have a “name” attribute valued “Default” OR “type” valued “Book”.

Condition Blocks
~~~~~~~~~~~~~~~~

There are basically six types of ``<condition_expression>`` blocks supported in py-ABAC: *Numeric*\ , *String*\ , *Collection*\ , *Object*\ , *Logic*\ , and *Other*. The JSON schema and examples for each are shown below:

:raw-html-m2r:`<u>Numeric Condition Block</u>`
""""""""""""""""""""""""""""""""""""""""""""""""""


*
  **Conditions:** ``Eq``\ , ``Neq``\ , ``Gt``\ , ``Gte``\ , ``Lt`` and ``Lte``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": <string>,
         "value": <number>
       }

    | **Field**     | **Description**                                       |
    | ------------- | ----------------------------------------------------- |
    | ``"condition"`` | Specifies the type of numeric condition.              |
    | ``"value"``     | Contains a number. This can be a float or an integer. |

  *
    **Description:**


    * ``Eq``\ : attribute value equals that in ``"value"``
    * ``Neq``\ : attribute value not equals that in ``"value"``
    * ``Gt``\ : attribute value is greater than that in ``"value"``
    * ``Gte``\ : attribute value is greater than equal to that in ``"value"``
    * ``Lt``\ : attribute value is less than that in ``"value"``
    * ``Lte``\ : attribute value is less than equal to that in ``"value"``

  *
    **Example:**

    .. code-block:: json

       {
         "condition": "Lte",
         "value": 1.5
       }

:raw-html-m2r:`<u>String Condition Block</u>`
"""""""""""""""""""""""""""""""""""""""""""""""""


*
  **Conditions:** ``Equals``\ , ``NotEquals``\ , ``Contains``\ , ``NotContains``\ , ``StartsWith``\ , ``EndsWith`` and ``RegexMatch``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": <string>,
         "value": <string>,
         "case_insensitive": <bool>
       }

    | **Field**            | **Description**                                              |
    | -------------------- | ------------------------------------------------------------ |
    | ``"condition"``        | Specifies the type of string condition.                      |
    | ``"value"``            | Contains a basic string or regex pattern.                    |
    | ``"case_insensitive"`` | String case insensitive condition flag. This is an optional field and by default is set to ``False``. |

  *
    **Description:**


    * ``Equals``\ : attribute value string equals that in ``"value"``
    * ``NotEquals``\ : attribute value string not equals that in ``"value"``
    * ``Contains``\ : attribute value contains the string in ``"value"``
    * ``NotContains``\ : attribute value does not contain the string in ``"value"``
    * ``StartsWith``\ : attribute value starts with string in ``"value"``
    * ``EndsWith``\ : attribute value ends with string in ``"value"``
    * ``RegexMatch``\ : attribute value string matches regex pattern in ``"value"``

  *
    **Example:**

    .. code-block:: json

       {
         "condition": "StartsWith",
         "value": "Cal"
       }

:raw-html-m2r:`<u>Collection Condition Block</u>`
"""""""""""""""""""""""""""""""""""""""""""""""""""""


*
  **Conditions:** ``AllIn``\ , ``AllNotIn``\ , ``AnyIn``\ , ``AnyNotIn``\ , ``IsIn`` and ``IsNotIn``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": <string>,
         "values": <list>
       }

    | **Field**     | **Description**                                              |
    | ------------- | ------------------------------------------------------------ |
    | ``"condition"`` | Specifies the type of collection condition.                  |
    | ``"values"``    | Collection of primitive type values like string, int ,float, etc. |

  *
    **Description:**


    * ``AllIn``\ : all members of attribute value collection are members of ``"values"``
    * ``AllNotIn``\ : none of the members of attribute value collection are members of ``"values"``
    * ``AnyIn``\ : one or more members of the attribute value collection are members of ``"values"``
    * ``AnyNotIn``\ : one or more members of the attribute value collection are not members of ``"values"``
    * ``IsIn``\ : attribute value (treated as a single value) is member of ``"values"``
    * ``IsNotIn``\ : attribute value (treated as a single value) is not member of ``"values"``

  *
    **Example:**

    .. code-block:: json

       {
         "condition": "AnyIn",
         "values": ["Example1", "Example2"]
       }

*
  **Conditions:** ``IsEmpty`` and ``IsNotEmpty``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": <string>
       }

    | **Field**     | **Description**                             |
    | ------------- | ------------------------------------------- |
    | ``"condition"`` | Specifies the type of collection condition. |

  *
    **Description:**


    * ``IsEmpty``\ : attribute value collection is empty
    * ``IsNotEmpty``\ : attribute value collection is not empty

  *
    **Example:**

    .. code-block:: json

       {
         "condition": "IsEmpty"
       }

:raw-html-m2r:`<u>Object Condition Block</u>`
"""""""""""""""""""""""""""""""""""""""""""""""""


*
  **Condition:** ``EqualsObject``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": "EqualsObject",
         "value": <object>
       }

    | **Field**     | **Description**                         |
    | ------------- | --------------------------------------- |
    | ``"condition"`` | Specifies the type of object condition. |
    | ``"value"``     | contains a JSON object                  |

  *
    **Description:**


    * ``EqualsObject``\ : attribute value JSON object equals that in ``"value"``

  *
    **Example:**

    .. code-block:: json

       {
         "condition": "EqualsObject",
         "value": {"name": "Sam"}
       }

:raw-html-m2r:`<u>Logic Condition Block</u>`
""""""""""""""""""""""""""""""""""""""""""""""""


*
  **Conditions:** ``AnyOf`` and ``AllOf``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": <string>,
         "values": <list<condition_expression>>
       }

    | **Field**     | **Description**                                     |
    | ------------- | --------------------------------------------------- |
    | ``"condition"`` | Specifies the type of logic condition.              |
    | ``"values"``    | Contains a list of ``<condition_expression>`` blocks. |

  *
    **Description:**


    * ``AnyOf``\ : attribute value satisfies any of the conditions in ``"values"``
    * ``AllOf``\ : attribute value satisfies all of the conditions in ``"values"``

  *
    **Example:**

    .. code-block:: json

       {
         "condition": "AllOf",
         "values": [
             {"condition": "Lt", "value": 1.5},
             {"condition": "Gt", "value": 0.5}
           ]
       }

*
  **Condition:** ``Not``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": "Not",
         "value": <condition_expression>
       }

    | **Field**     | **Description**                            |
    | ------------- | ------------------------------------------ |
    | ``"condition"`` | Specifies the ``"Not"`` logic condition.     |
    | ``"value"``     | Contains a ``<condition_expression>`` block. |

  *
    **Description:**


    * ``Not``\ : attribute value does not satisfy the condition in ``"value"``

  *
    **Example:**

    .. code-block:: json

       {
           "condition": "Not",
           "value": {"condition": "Eq", "value": 1.5}
       }

:raw-html-m2r:`<u>Other Condition Block</u>`
""""""""""""""""""""""""""""""""""""""""""""""""


*
  **Condition:** ``CIDR``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": "CIDR",
         "value": <string>
       }

    | **Field**     | **Description**                           |
    | ------------- | ----------------------------------------- |
    | ``"condition"`` | Specifies the ``"CIDR"`` network condition. |
    | ``"value"``     | Contains a CIDR block as string.          |

  *
    **Description:**


    * ``CIDR``\ : IP address in attribute value is within the CIDR block in ``"value"``

  *
    **Example:**

    .. code-block:: json

       {
           "condition": "CIDR",
           "value": "10.0.0.0/16"
       }

*
  **Condition:** ``EqualsAttribute``


  *
    **JSON Schema:**

    .. code-block::

       {
         "condition": "EqualsAttribute",
         "ace": <string>,
         "path": <string>
       }

    | **Field**     | **Description**                                              |
    | ------------- | ------------------------------------------------------------ |
    | ``"condition"`` | Specifies the ``"EqualsAttribute"`` condition.                 |
    | ``"ace"``       | Specifies access control element. The value for this field should be either ``"subject"``\ , ``"resource"``\ , ``"action"``\ , or ``"context"``. |
    | ``"path"``      | Specified the attribute path in ObjectPath notation of the access control element in ``"ace"``. |

  *
    **Description:**


    * ``EqualsAttribute``\ : attribute value equals the value of attribute at location ``"path"`` of ``"ace"`` access control element

  *
    **Example:**

    .. code-block:: json

       {
           "condtion": "EqualsAttribute",
           "ace": "context",
           "path": "$.network.name"
       }

*
  **Conditions:** ``Any``\ , ``Exists`` and ``NotExists``


  *
    **JSON Schema:**

    .. code-block::

         {
           "condition": <string>
         }

    | **Field**     | **Description**                  |
    | ------------- | -------------------------------- |
    | ``"condition"`` | Specifies the type of condition. |

  *
    **Description:**


    * ``Any``\ : attribute contains any value, null value included
    * ``Exists``\ : attribute exists  – null value is checked
    * ``NotExists``\ : attribute does not exits – null value is checked

  *
    **Example:**

    .. code-block:: json

       {
           "condition": "Any"
       }

*\ `Back to top <#py-abac>`_\ *

Access Request JSON
-------------------

An access request is a data object sent by PEP to PDP. This object contains all the information needed by the PDP to evaluate the policies and return access decision. The JSON schema of the object is given by

.. code-block:: json

   {
       "subject": {
           "id": "<string>",
           "attributes": "<attribute_block>"
       },
       "resource": {
           "id": "<string>",
           "attributes": "<attribute_block>"
       },
       "action": {
           "id": "<string>",
           "attributes": "<attribute_block>"
       },
       "context": "<attribute_block>"
   }

where ``<attribute_block>`` is just a JSON block containing one or more attribute-value pairs. An example request is shown below:

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
