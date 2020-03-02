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

.. include:: blocks/targets.rst

.. _rules_block:

.. include:: blocks/rules.rst

.. _conditions_blocks:

.. include:: blocks/conditions.rst
