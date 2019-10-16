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
	- [Storage](#storage)
	    - [Memory](#memory)
	    - [MongoDB](#mongodb)
	    - [SQL](#sql)
	- [Migration](#migration)
	- [AttributeProvider](#attributeprovider)
	- [EvaluationContext](#evaluationcontext)
- [Policy Language](#policy-language)
  - [Policy JSON](#policy-json)
    - [Targets vs Rules](#targets-vs-rules)
    - [Targets Block](#targets-block)
    - [Rules Block](#rules-block)
    - [Condition Blocks](#condition-blocks)
  - [Access Request](#access-request)
- [Logging](#logging)
- [Milestones](#milestones)
- [Acknowledgements](#acknowledgements)
- [Development](#development)
- [License](#license)

---

## Introduction

Py-ABAC is an attribute-based access control ([ABAC](https://en.wikipedia.org/wiki/Attribute-based_access_control)) toolkit based on policies. ABAC gives you a fine-grained control on definition of the rules that restrict an access to resources and is generally considered a "next generation" authorization model. The design of py-ABAC stems from the [XACML](https://en.wikipedia.org/wiki/XACML) standard, and the ABAC python SDK [Vakt](https://github.com/kolotaev/vakt).

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

This is the main object containing rules for accessing resources. A policy object can be created by first defining a policy JSON using the JSON-based [Policy Language](#policy-language), and then parsing it using the `Policy` class.  

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

See the [Policy Language](#policy-language) section for detailed description of JSON structure.

*[Back to top](#py-abac)*

### Request

A `Request` object represents the access request generated by PEP in the ABAC architecture. All you need to do is take any kind of incoming user request (REST request, SOAP, etc.) and build a `Request` object out of it in order to feed it to py-ABAC. 

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

You might have noticed the presence of empty  `"id"` fields for the `subject`, `resource` and `action` access control elements in the above example. These are called _target IDs_ and are mandatory fields for creating an access request object in py-ABAC. The purpose of these fields is explained in detail in the [Target Block](#targets-block) subsection of [Policy Language](#policylanguage). If you are unsure of their usage, you can safely set them to an empty string.

*[Back to top](#py-abac)*

### PDP

This component is the policy decision point, instantiated through the `PDP` class. It is the main entry point of py-ABAC for evaluating policies. At a minimum, a [Storage](#storage) object is required to create a `PDP` object. It has one method, `is_allowed`, which when passed a `Request` object, gives you a boolean answer: is access allowed or not?

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

By default, a `PDP` object uses the `DenyOverrides` algorithm for policy evaluation. To specify otherwise, pass the evaluation algorithm at creation. Moreover, a list of [AttributeProvider](#attributeproviders) objects can also be provided. 

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

*[Back to top](#py-abac)*

### Storage

The `Storage` is a component which provides interface for implementing policy persistence. It provides the following methods:

```python
# Store a Policy
add(policy)                 

# Retrieve a Policy by its ID
get(uid)                    

# Retrieve all stored Policies (with pagination)
get_all(limit, offset)      

# Store an updated Policy
update(policy)              

# Delete Policy from storage by its ID
delete(uid)                 

# Retrieve Policies that match the given target IDs
get_for_target(subject_id, resource_id, action_id) 
```

Storage may have various backend implementations (RDBMS, NoSQL databases, etc.). py-ABAC ships some Storage implementations out of the box. See below.

##### Memory

Will be part of v0.2.1

##### MongoDB

MongoDB is chosen as the most popular and widespread NO-SQL database.

```python
from pymongo import MongoClient
from py_abac.storage import MongoStorage

client = MongoClient('localhost', 27017)
storage = MongoStorage(client, 'database-name', collection='optional-collection-name')
```

Default database and collection names are 'py_abac' and  'py_abac_policies' respectively.

Actions are the same as for any Storage that conforms interface of `py_abac.storage.base.StorageBase` base class.

##### SQL

Will be part of v0.2.2

*[Back to top](#py-abac)*

#### Migration

`py_abac.storage.migration` is a set of components that are useful for [Storage](#storage). The design and implementation is taken from the [Vakt](https://github.com/kolotaev/vakt) SDK. It's recommended in favor over manual actions on DB schema/data since it's aware of py-ABAC requirements. But it's not mandatory. It is up to a particular Storage to decide whether it needs migrations. It consists of 3 components:

- `Migration`
- `MigrationSet`
- `Migrator`

`Migration` allows you to describe data modifications between versions. Each storage can have a number of `Migration` classes to address different releases with the order of the migration specified in `order` property. The class should be located inside corresponding storage module and should implement `py_abac.storage.migration.Migration`. Migration has 2 main methods (as you might guess) and 1 property:

- `up` - runs db "schema" upwards
- `down` - runs db "schema" downwards (rolls back the actions of `up`)
- `order` - tells the number of the current migration in a row

`MigrationSet` is a component that represents a collection of Migrations for a Storage. You should define your own migration-set. It should be located inside particular storage module and implement `py_abac.storage.migration.MigrationSet`. It has 3 methods that lest unimplemented:

- `migrations` - should return all initialized Migration objects
- `save_applied_number` - saves a number of a lst applied up migration in the Storage for later reference
- `last_applied` - returns a number of a lst applied up migration from the Storage

`Migrator` is an executor of a migrations. It can execute all migrations up or down, or execute a particular migration if `number` argument is provided.

Example usage:

```python
from pymongo import MongoClient
from py_abac.storage.mongo import MongoStorage, MongoMigrationSet
from py_abac.storage.migration import Migrator

client = MongoClient('localhost', 27017)
storage = MongoStorage(client, 'database-name', collection='optional-collection-name')

migrator = Migrator(MongoMigrationSet(storage))
migrator.up()
...
migrator.down()
...
migrator.up(number=2)
...
migrator.down(number=2)
```

*[Back to top](#py-abac)*

### AttributeProvider

 `AttributeProvider` is an interface to create a PIP. The purpose of this object is to provide attribute values missing in the `Request` object. During policy evaluation, the `PDP` first checks the `Request` object for attribute values; If no values are found, it then checks the list of `AttributeProvider`objects passed during creation. In order to create an `AttributeProvider` object, you need to implement the `get_attribute_value` method. 

```python
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
```

As seen in the above example, the `get_attribute_value` method takes in three arguments: `ace`, `attribute_path` and `ctx`. The `ace` is a string value indicating for which access control element the attribute value is being requested. This argument will be set to either `"subject"`, `"resource"`, `"action"`, or `"context"`. The `attribute_path` argument is a string in  [ObjectPath](http://objectpath.org/) notation denoting the attribute for which the value is being requested. The `ctx` argument is an [EvaluationContext](#evaluationcontext) object. The primary purpose of this argument is to retrieve values of other attributes. A common use-case would be to return values conditioned upon the values of other attributes.

```python
# An email attribute provider class
class EmailAttributeProvider(AttributeProvider):
    def get_attribute_value(self, ace, attribute_path, ctx):
        # Return email for Max
        if ctx.get_attribute_value("subject", "$.name") == "Max":
            return "max@gmail.com"
        # Else return default email
        return "default@gmail.com"
```

Lastly, if the `AttributeProvider` does not contain value for an attribute, the `get_attribute_value` must return `None`.

*[Back to top](#py-abac)*

### EvaluationContext

An `EvaluationContext` object is created by the `PDP` during policy evaluation. This object is used by the `PDP` for retrieval of attribute values for which the policy is defined. It has following properties:

```python
# The target ID for subject access control element
ctx.subject_id  

# The target ID for resource access control element
ctx.resource_id

# The target ID for action access control element
ctx.action_id

# Lookup a value for an attribute of an access control element
ctx.get_attribute_value(ace: str, attribute_path: str)
```
During retrieval,  the `EvaluationContext` first checks for attribute value in the `Request` object. If the value is not found, it then checks all the `AttributeProvider` objects sequentially.

*[Back to top](#py-abac)*

## Policy Language

This section presents the JSON-based policy language for py-ABAC. There are two subsections. The first subsection discusses JSON structure of a policy, while the latter about the access request. 

### Policy

A policy structure consists of `uid`, `description`, `conditions`, `targets`, `effect`, and `priority` fields. The JSON schema is given by

```
{   
    "uid": <string>,  
    "description": <string>,   
    "rules": <rules_block>,   
    "targets": <targets_block>,   
    "effect": <string>,   
    "priority": <number> 
}
```

where `<rules_block>` and `<targets_block>` are JSON blocks discussed in detail in the [Rules Block](#rules-block) and [Targets Block](#targets-block) subsections. Essentially, the `"targets"` and `"rules"` fields are used to define conditions on the attributes of access control elements. When these conditions are satisfied, the policy applies and the value for the `"effect"` field is returned by the `PDP`. Thus `"effect"` is the returned decision of the policy and can be either `"allow"` or `"deny"`. The  `"uid"` field is a string value that uniquely identifies a policy. As the name suggests, the `"description"` field stores description of the policy. Finally, `"priority"` provides a numeric value indicating the weight of the policy when its decision conflicts with other policy under the `HighestPriority` evaluation algorithm. By default, this field is set to `0` for all policies.

#### Targets vs Rules

The concept of `"targets"` and `"rules"` in py-ABAC is derived from the XACML standard. Both are used to define conditions on attributes during policy creation. There is however a basic distinction between the two. This distinction will become more clear in the following sections. From a conceptual standpoint, `"targets"` states for which access control elements a policy applies. In other words, targets of a policy. The `"rules"` on the other-hand define the conditions on the attributes of the targets. To illustrate this point, lets consider a system with two users, "Sam" and "John". Each user has an attribute called "age".  Suppose we want to create a policy where "Sam" can access the system only if he is above 18 years old. To achieve this, we set the target of the policy to "Sam" while the rule to the condition "age" > 18. The exact syntax to do so is shown in the following sections.

#### Targets Block

The targets block specifies for which access control elements a policy applies. This block contains one or more 'ID' attribute values for `subject`, `resource`, and `action` fields. Thus in py-ABAC it is mandatory that these three access control elements have a string valued ID attribute in the `Request` object. The JSON schema for the block is

```
{   
    "subject_id": ["<id_string>", "<id_string>", ... ],   
    "resource_id": ["<id_string>", "<id_string>", ... ],   
    "action_id": ["<id_string>", "<id_string>", ... ] 
} 
```

where  `<id_string>` denotes string values of the ‘ID’ attribute. The array here acts as an implicit OR operator. Furthermore wild-carded values for `<id_string>` are also supported:

```json
{   
    "subject_id": ["a", "b"],   
    "resource_id": ["ab*"],   
    "action_id": ["*"] 
}
```

This example states that the policy is only applicable when the subject ID is either set to “a” or “b”, and when the resource ID starts with “ab”. The action can have any ID value. 

For convince, the array can be omitted when only a single `<id_string>` is to be set for a filed. Thus the above target block can also be defined as

```json
{   
    "subject_id": ["a", "b"],   
    "resource_id": "ab*",   
    "action_id": "*" 
}
```

Note that when no target block is explicitly specified, the policy is considered to be applicable for all targets as py-ABAC uses the following default: 

```json
{   
    "subject_id": "*",   
    "resource_id": "*",   
    "action_id": "*" 
}   
```

#### Rules Block

Rules are Boolean expressions defined on the attributes of the targeted access control elements. The JSON schema is given by

```json
{   
    "subject": "<boolean_expression>",   
    "resource": "<boolean_expression>",   
    "action": "<boolean_expression>",   
    "context": "<boolean_expression>" 
} 
```
with `<boolean_expression>` being a JSON block for Boolean expression.

A policy is considered applicable only when each of the Boolean expressions are satisfied. These expressions define constraints on the attribute values of the access control elements. The constraints can be as simple as those involving only a single attribute, or can be complex involving multiple attributes. A simple Boolean expression consists of a key-value pair as shown below:

```json
{"<attribute_path>": "<condition_expression>"}
```

The key specifies the attribute in [ObjectPath](http://objectpath.org/) notation while the value is a conditional expression. The `<condition_expression>` is again a JSON block specifying the requirements that the attribute value needs to meet. The different supported condition expressions are shown in [Condition Blocks](#condition-blocks) subsection. As an example, the conditional block for the requirement that "name" attribute of subject field should be "Max" is shown below:

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

Sometimes conditions on a single attribute does not suffice and constraints on multiple attributes connected by logical relations like AND or OR are required. In py-ABAC, this is achieved by using in-built JSON data structures *object* and *array* as implicit logical operators. An *object* is implicitly an AND operator which would be evaluated to true only if all the included key-value pairs are evaluated to true. Similarly, an *array* is implicitly an OR operator which would be evaluated to true as long as at least one of its members is evaluated to true. For an example see the following conditional blocks:

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

The overall rule states that the subject should have an attribute "firstName" valued "Carl" AND "lastName" valued "Rubin". Similarly, the resource should have an attribute "name" valued "Default" OR "type" valued "Book".

#### Condition Blocks

There are basically six types of `<condition_expression>` blocks supported in py-ABAC: *Logic,* *Numeric*, *String*, *Collection*, Object, and *Other*. The JSON schema and examples for each are shown below:

##### Logic Condition Block

| **JSON Schema**                                              | **Description**                                              | **Example**                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ```{   "condition": "<string>",   "values": "<list<ConditionJson>> "}<br />``` | *condition*: specifies the type of logic condition. The different possible values are: "AllOf": perform logical AND operation on items in *values*"AnyOf": perform logical OR operation on items in *values* *values*: contains a list of ConditionJSON objects | {   "condition": "AllOf",   "values": [   {     "condition": "Lt",     "value": 1.5   },   {     "condition": "Gt",     "value": 0.5   }] } |
| {   "condition": "Not",   "value": <ConditionJson> }         | *condition*: specifies logic "Not" condition.  *value*: contains a ConditionJSON object | {   "condition": "Not",   "value": {     "condition": "Eq",     "value": 1.5   } } |

##### Numeric Condition Block

| **JSON Schema**                                  | **Description**                                              | **Example**                                  |
| ------------------------------------------------ | ------------------------------------------------------------ | -------------------------------------------- |
| {   "condition": <string>,   "value": <number> } | *condition*: specifies the type of numeric condition. The different possible values are: "Eq": attribute value is equal to that in *value*"Gt": attribute value is greater than that in *value*"Lt": attribute value is less than that in *value*"Gte": attribute value is greater than equal to that in *value*"Lte": attribute value is less than equal to that in *value* *value*: contains a number. This can be a float or an int. | {     "condition": "Lte",     "value": 1.5 } |

##### Collection Condition Block

| **JSON Schema**                                | **Description**                                              | **Example**                                                  |
| ---------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| {   "condition": <string>,  "values": <list> } | *condition*: specifies the type of collection condition. The different possible values are: "AnyIn": one or more of the values for attribute are in *values*"AllIn": all the values for attribute are in *values* *values*: collection of primitive type values like string, int ,float, etc | {     "condition": "AnyIn",     "values": [      "Example1",       "Example2"    ] } |

##### Object Condition Block

##### Other Condition Block

| **JSON Schema**                                | **Description**                                              | **Example**                                                |
| ---------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| {   "condition": "CIDR",   "value": <string> } | *condition*: specifies "CIDR" network block condition. The attribute value should be an IP address within the CIDR block to satisfy this condition. *values*: CIDR block as string type | {     "condition": "CIDR",     "value": "192.168.0.0/16" } |
| {   "condition": "Any" }                       | *condition*: specifies "Any" condition. The attribute can have any value. This condition only fails when the attribute for which this condition is defined does not exist. | {   "condition": "Any" }                                   |
| {   "condition": "Exists" }                    | *condition*: specifies "Exists" condition. This condition is satisfied when the attribute for which this condition is defined exists. | {   "condition": "Exists" }                                |

*[Back to top](#py-abac)*

### Access Request

An access request is a data object sent by PEP to PDP. This object contains all the information needed by the PDP to evaluate the policies and return access decision. The JSON schema of the object is given by

```json
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

*[Back to top](#py-abac)*

## Logging

py-ABAC follows a common logging pattern for libraries:

Its corresponding modules log all the events that happen but the log messages by default are handled by `NullHandler`. It's up to the outer code/application to provide desired log handlers, filters, levels, etc.

For example:

```python
import logging

root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(logging.StreamHandler())

... # here go all the py_abac calls.
```

*[Back to top](#py-abac)*

## Milestones

Most valuable features to be implemented in the order of importance:

-  In-Memory Storage
-  SQL Storage
-  Caching mechanism for Storage
-  YAML-based language for declarative policy definitions
-  File Storage

*[Back to top](#py-abac)*

## Acknowledgements

The conceptual and implementation design of py-ABAC stems from the [XACML](https://en.wikipedia.org/wiki/XACML) standard and the ABAC python SDK [Vakt](https://github.com/kolotaev/vakt).

*[Back to top](#py-abac)*

## Development

To hack py-ABAC locally run:

```
$ pip install -e .[dev]  		   				# to install all dependencies
$ docker run --rm -d -p 27017:27017 mongo		# Run mongodb server on docker
$ pytest --cov=py_abac tests/      				# to get coverage report
$ pylint py_abac                   				# to check code quality with PyLint
```

Optionally you can use `make` to perform development tasks.

*[Back to top](#py-abac)*

## License

The source code is licensed under Apache License Version 2.0

*[Back to top](#py-abac)*