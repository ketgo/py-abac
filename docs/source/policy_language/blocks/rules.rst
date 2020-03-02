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
