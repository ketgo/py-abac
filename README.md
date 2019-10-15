# py-ABAC
Attribute Based Access Control (ABAC) for python. 

[![Build Status](https://travis-ci.com/ketgo/py-abac.svg?token=oCVxhfjJAa2zDdszGjoy&branch=master)](https://travis-ci.com/ketgo/py-abac)
[![codecov.io](https://codecov.io/gh/ketgo/pyabac/coverage.svg?branch=master)](https://codecov.io/gh/ketgo/pyabac/coverage.svg?branch=master)
[![Apache 2.0 licensed](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://raw.githubusercontent.com/kolotaev/vakt/master/LICENSE)

---

- [Introduction](#introduction)
- [Install](#install)
- [Usage](#usage)
- [Concepts](#concepts)
- [Components](#components)
	- [Policy](#policy)
	- [Request](#inquiry)
	- [PDP](#pdp)
	- [AttributeProvider](#attributeprovider)
	- [Storage](#storage)
	    - [Memory](#memory)
	    - [MongoDB](#mongodb)
	    - [SQL](#sql)
	- [Migration](#migration)
- [Policy Language](#policylanguage)
- [Logging](#logging)
- [Examples](./examples)
- [Milestones](#milestones)
- [Acknowledgements](#acknowledgements)
- [Development](#development)
- [License](#license)

---

## Introduction

Py-ABAC is an attribute-based access control ([ABAC](https://en.wikipedia.org/wiki/Attribute-based_access_control)) toolkit based on policies. ABAC gives you a fine-grained control on definition of the rules that restrict an access to resources and is generally considered a "next generation" authorization model. The design of py-ABAC stems from the [XACML](https://en.wikipedia.org/wiki/XACML) standard, and the ABAC python SDK [vakt](https://github.com/kolotaev/vakt).

See [concepts](#concepts) section for more details.

*[Back to top](#py-abac)*


## Install

PyABAC runs on Python >= 3.5. PyPy implementation is supported as well.


To install run the following:
```bash
pip install py-abac
```

*[Back to top](#py-abac)*

## Usage

A quick dive-in:

```python
from pymongo import MongoClient
from py_abac import PDP, Policy, Request
from py_abac.storage import MongoStorage

# Policy definition in JSON
policy_json = {
    "uid": "1",
    "description": "Max and Nina are allowed to create, delete, get any "
                   "resources only if the client IP matches.",
    "effect": "allow",
    "rules": {
        "subject": [{"$.name": {"condition": "Equals", "value": "Max"}},
                    {"$.name": {"condition": "Equals", "value": "Nina"}}],
        "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
        "action": [{"$.method": {"condition": "Equals", "value": "create"}},
                   {"$.method": {"condition": "Equals", "value": "delete"}},
                   {"$.method": {"condition": "Equals", "value": "get"}}],
        "context": {"$.ip": {"condition": "CIDR", "value": "127.0.0.1/32"}}
    },
    "targets": {},
    "priority": 0
}
# Parse JSON and create policy object
policy = Policy.from_json(policy_json)

# Setup policy storage
client = MongoClient()
storage = MongoStorage(client)
# Add policy to storage
storage.add(policy)

# Create policy decision point
pdp = PDP(storage)

# A sample access request JSON
request_json = {
    "subject": {
        "id": "", 
        "attributes": {"name": "Max"}
    },
    "resource": {
        "id": "", 
        "attributes": {"name": "myrn:example.com:resource:123"}
    },
    "action": {
        "id": "", 
        "attributes": {"method": "get"}
    },
    "context": {
        "ip": "127.0.0.1"
    }
}
# Parse JSON and create access request object
request = Request.from_json(request_json)

# Check if access request is allowed. Evaluates to True since 
# Max is allowed to get any resource when client IP matches.
assert pdp.is_allowed(request)
```

For more examples see [here](./examples).

*[Back to top](#py-abac)*

## Concepts

### Access Control Architecture

![img](https://lh6.googleusercontent.com/z4oppCjtEITgem5UZUN28NiaV4LrYPrjqD1MjZiYDhjmj1OkFFcN9H2jj64Zd0tkRkf5O436eOA574Sur0uSDlUztRtadREn_wfRfMbh4dNiACxivd0zjM_gLcF94N-bdhl_g15N)

The above diagram depicts the standard architecture for ABAC, which is as follows:

1. The PEP or Policy Enforcement Point: It is your piece of code that uses py-ABAC to protect  app & data. The PEP should  inspect a user request, create a corresponding access request, and send it to the PDP for evaluation.

2. The PDP or Policy Decision Point is the brain of the architecture. This is the piece which evaluates incoming access requests against policies and returns a Permit / Deny decision. The PDP may also use PIPs to retrieve missing attribute values during policy evaluation.

3. The PIP or Policy Information Point bridges the PDP to external sources of attribute values e.g. LDAP or databases. 

4. The PAP or Policy Administration Point: manages the creation, update and deletion of policies evaluated by PDP. 

*[Back to top](#py-abac)*

### Access Control Elements

In the above architecture, following four elements are involved during an access request to PDP:

1. `subject`: This is the entity which requests access, also known as the request principal. A subject can be anything that requests access, i.e. a user or an application.
2. `resource`: The object which is requested to be accessed by the subject. 
3. `action`: The action being performed on the resource.
4. `context`: This element deals with time, location or dynamic aspects of the access control scenario. 

In py-ABAC one defines policies containing conditions on one or more attributes of these four elements. If these conditions are satisfied, an access decision is returned by the PDP using an evaluation algorithm. There are three different evaluation algorithms supported by py-ABAC:

1. `AllowOverrides`: returns `allow` if any decision evaluates to `allow`; and returns `deny` if all decisions evaluate to `deny`.
2. `DenyOverrides`: returns `deny` if any decision evaluates to `deny`; returns `allow` if all decisions evaluate to `allow`.
3. `HighestPriority`: returns the highest priority decision that evaluates to either `allow` or `deny`. If there are multiple equally highest priority decisions that conflict, then `DenyOverrides` algorithm would be applied among those highest priority decisions.

*[Back to top](#py-abac)*

## Components

### Policy

This is the main object containing rules for accessing resources. A policy object can be created by first defining a policy JSON using the JSON-based [Policy Language](##Policy Language), and then parsing it using the `Policy` class.  

``` python
from py_abac import Policy

# Policy definition in JSON-based policy language
policy_json = {
    "uid": "1",
    "description": "Max is not allowed to create, delete, get any resource",
    "effect": "deny",
    "rules": {
        "subject": {"$.name": {"condition": "Equals", "value": "Max"}},
        "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
        "action": [{"$.method": {"condition": "Equals", "value": "create"}},
                   {"$.method": {"condition": "Equals", "value": "delete"}},
                   {"$.method": {"condition": "Equals", "value": "get"}}],
        "context": {}
    },
    "targets": {},
    "priority": 0
}
# Prase policy JSON to create Policy object
policy = Policy.from_json(policy_json)
```

See the [Policy Language](##Policy Language) section for detailed description of JSON structure.

*[Back to top](#py-abac)*

### Request

The access request generated by PEP in the ABAC architecture is created using the `Request` object in py-ABAC. All you need to do is take any kind of incoming user request (REST request, SOAP, etc.) and build a `Request` object out of it in order to feed it to py-ABAC. 

```python
from py_abac import Request
from flask import request, session

# Create a access request JSON from flask request object
request_json = {
    "subject": {
        "id": "", 
        "attributes": {"name": request.values.get("username")}
    },
    "resource": {
        "id": "", 
        "attributes": {"name": request.path}
    },
    "action": {
        "id": "", 
        "attributes": {"method": request.method}
    },
    "context": {}
}
# Parse JSON and create access request object
request = Request.from_json(request_json)
```

You might have noticed the presence of empty  `"id"` fields for the `subject`, `resource` and `action` access control elements in the above example. These are mandatory fields for creating an access request object in py-ABAC. The purpose of these fields is explained in detail in the [Policy Language](##Policy Language) section. If unsure of their usage, you can safely set them to an empty string.

### PDP

You can create a policy decision point by the instantiating the `PDP` class. It is the main entry point of py-ABAC for evaluating access requests. At a minimum a [Storage](#storage) object is needed to create a `PDP` object. It has one method `is_allowed` when passed a `Request` object gives you a boolean answer: is access allowed or not?

```python
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
```



By default, a `PDP` object uses the `DenyOverrides` algorithm for policy evaluation. To specify otherwise, pass the evaluation algorithm at time of creation. Furthermore, a list of [AttributeProvider](#attributeproviders) objects can also be specified. 

```python
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
```

The three supported algorithms are `EvaluationAlgorithm.DENY_OVERRIDES`, `EvaluationAlgorithm.ALLOW_OVERRIDES`, and `EvaluationAlgorithm.HIGHEST_PRIORITY`.

### AttributeProvider

### Storage

## Policy Language

We now present the policy language used by **pyabac**. This section is divided into two subsections. The first subsection discusses JSON-based definition of a policy, while the latter about access request. 

#### Policy

A policy object consists of id, description, conditions, targets, effect, and priority fields. The JSON schema of this object is given by

```json
{   
    "id": <string>,  
    "description": <string>,   
    "rules": <rules_block>,   
    "targets": <targets_block>,   
    "effect": <string>,   
    "priority": <number> 
}
```

where `<conditions_block>` and `<targets_block>` are JSON blocks explained in the following sections. The `"id"` field is a string value that uniquely identifies a policy. The `"description"` stores description of the policy provided by the policy creator. The two fields `"rules"` and `"targets"` indicate the attributes of the access control elements to which the policy apply. The `"effect"` is the returned decision of the policy and can be either *allow* or *deny*. Finally, `"priority"` provides a numeric value indicating the weight of the policy when its decision conflicts with other policy under the `HighestPriority` evaluation algorithm. By default, this field is set to `0` for all policies.

##### Rules Block

Rules are Boolean expressions defined on the attributes of the access control elements. This block consists of fields subject, resource, action and context, where for each field a Boolean expression is defined on their attributes. The JSON schema is given by

```json
{   
    "subject": <boolean_expression>,   
    "resource": <boolean_expression>,   
    "action": <boolean_expression>,   
    "context": <boolean_expression> 
} 
```

with `<boolean_expression>` being a JSON block for Boolean expression.

A policy is considered applicable only when each of the Boolean expressions are satisfied. These expressions are constraints on the attribute values of the field for which they are defined. These constraints can be simple, involving only a single attribute, or can be complex consisting of multiple attributes. A simple Boolean expression consists of a key-value pair as shown below:

```json
{"<attribute_path>": <condition_expression>}
```

The key specifies an attribute path in *ObjectPath* format while the value is a condition expression. The condition expression is a JSON block specifying specifically the requirements that the attribute value needs to meet. The different supported condition expressions by **pyabac** are shown in Appendix. As an example, the condition block for the requirement that name attribute of subject field should be Max is shown below:

```json
{
    "subject": {     
        "$.name": {       
            "condition": "Eq",       
            "value": "Max"     
        }   
    } 
}
```

Sometimes condition on a single attribute does not suffice and constraints on multiple attributes connected by logical relations like AND or OR are required. In **pyabac** this is achieved by using JSON’s in-built data structures, *object* and *array*, as implicit logical operators. An *object* is implicitly an AND operator which would be evaluated to true only if all the included key-value pairs are evaluated to true. Similarly, an *array* is implicitly a OR operator which would be evaluated to true as long as at least one of its members is evaluated to true. This is illustrated in the following condition block:

```json
{   
    "subject": {     
        "$.firstName": {       
            "condition": "Eq",
            "value": "Carl"
        }
    },   
    "$.lastName": {     
        "condition": "Eq",     
        "value": "Rubin"   
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
```

The condition states that the subject should have an attribute `firstName` as "Carl" AND `lastName` as "Rubin". Similarly, the resource should have an attribute name as "Default" OR type as "Book".

##### Targets Block

The primary purpose of targets block is to define for which elements the policy applies. The block contains an implicit logical OR operation on ‘ID’ attribute of the subject, resource, and action fields. This enables an efficient retrieval of policies from a repository by PDP. Thus in **pyabac**, it is required that these access elements have a string valued ID attribute. The JSON schema of the block is given by

```json
{   
    "subject_id": [<id_string>, <id_string>, … ],   
    "resource_id": [<id_string>, <id_string>, … ],   
    "action_id": [<id_string>, <id_string>, … ] 
} 
```

where <id_string> are the required string values for the ‘ID’ attribute. Regex values for <id_string> are also allowed. An example target block is shown below:

```json
{   
    "subject_id": ["a", "b"],   
    "resource_id": ["ab.*"],   
    "action_id": [".*"] 
}
```

This target block defines that the policy is only applicable if the subject ID is either set to “a” or “b”, and the resource ID starts with string “ab”. The action can have any ID value. 

If a target block is not explicitly specified, the policy is considered to be always applicable with the following default used: 

```json
{   
    "subject_id": [".*"],   
    "resource_id": [".*"],   
    "action_id": [".*"] 
}
```

#### Access Request

An access request is a data object sent by PEP to PDP. This object contains all the information needed by the PDP to evaluate the policies and return access decision. The JSON schema of the object is given by

```json
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
```

where `<attribute_block>` is just a JSON block containing one or more attribute-value pairs. An example request is shown below:

```json
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
```

### Appendix

There are basically six types of condition expressions supported in **pyabac**: *Logic,* *Numeric*, *String*, *Collection*, *Attribute*, and *Other*. The JSON schema for each are shown below:

| **Logic**                                                    |                                                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **JSON Schema**                                              | **Description**                                              | **Example**                                                  |
| {   "condition": <string>,   "values": <list<ConditionJson>> } | *condition*: specifies the type of logic condition. The different possible values are: "AllOf": perform logical AND operation on items in *values*"AnyOf": perform logical OR operation on items in *values* *values*: contains a list of ConditionJSON objects | {   "condition": "AllOf",   "values": [   {     "condition": "Lt",     "value": 1.5   },   {     "condition": "Gt",     "value": 0.5   }] } |
| {   "condition": "Not",   "value": <ConditionJson> }         | *condition*: specifies logic "Not" condition.  *value*: contains a ConditionJSON object | {   "condition": "Not",   "value": {     "condition": "Eq",     "value": 1.5   } } |

| **Numeric**                                      |                                                              |                                              |
| ------------------------------------------------ | ------------------------------------------------------------ | -------------------------------------------- |
| **JSON Schema**                                  | **Description**                                              | **Example**                                  |
| {   "condition": <string>,   "value": <number> } | *condition*: specifies the type of numeric condition. The different possible values are: "Eq": attribute value is equal to that in *value*"Gt": attribute value is greater than that in *value*"Lt": attribute value is less than that in *value*"Gte": attribute value is greater than equal to that in *value*"Lte": attribute value is less than equal to that in *value* *value*: contains a number. This can be a float or an int. | {     "condition": "Lte",     "value": 1.5 } |

| **Collection**                                 |                                                              |                                                              |
| ---------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **JSON Schema**                                | **Description**                                              | **Example**                                                  |
| {   "condition": <string>,  "values": <list> } | *condition*: specifies the type of collection condition. The different possible values are: "AnyIn": one or more of the values for attribute are in *values*"AllIn": all the values for attribute are in *values* *values*: collection of primitive type values like string, int ,float, etc | {     "condition": "AnyIn",     "values": [      "Example1",       "Example2"    ] } |

| **Other**                                      |                                                              |                                                            |
| ---------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| **JSON Schema**                                | **Description**                                              | **Example**                                                |
| {   "condition": "CIDR",   "value": <string> } | *condition*: specifies "CIDR" network block condition. The attribute value should be an IP address within the CIDR block to satisfy this condition. *values*: CIDR block as string type | {     "condition": "CIDR",     "value": "192.168.0.0/16" } |
| {   "condition": "Any" }                       | *condition*: specifies "Any" condition. The attribute can have any value. This condition only fails when the attribute for which this condition is defined does not exist. | {   "condition": "Any" }                                   |
| {   "condition": "Exists" }                    | *condition*: specifies "Exists" condition. This condition is satisfied when the attribute for which this condition is defined exists. | {   "condition": "Exists" }                                |

