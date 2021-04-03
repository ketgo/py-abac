"""
    `EqualsAttribute` condition example.
"""

from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.memory import MemoryStorage

# Policy definition in JSON
policies_json = [
    {
        "uid": "2",
        "description": "Allow user to get his own account",
        "effect": "allow",
        "rules": {
            "subject": {
                "$.user_id": {
                    "condition": "RegexMatch",
                    "value": ".*"
                }
            },
            "resource": {
                "$.path": {
                    "condition": "RegexMatch",
                    "value": "^\/v1\/user\/[0-9a-zA-Z]{24}$"
                },
                "$.id": {
                    "condition": "EqualsAttribute",
                    "ace": "subject",
                    "path": "$.user_id"
                }
            },
            "action": {
                "$.method": {
                    "condition": "IsIn",
                    "values": [
                        "get"
                    ]
                }
            },
            "context": {}
        },
        "targets": {
            "resource_id": "/v1/user"
        },
        "priority": 0
    }
]

# Setup policy storage
storage = MemoryStorage()
# Add policy to storage
for policy_json in policies_json:
    # Parse JSON and create policy object
    policy = Policy.from_json(policy_json)
    storage.add(policy)

# Create policy decision point
pdp = PDP(storage)

# A sample access request JSON
requests_json = [
    # Get account by 604g7bh4av2aj54114c14600 --> Should be allowed.
    {
        "subject": {
            "id": "",
            "attributes": {
                "user_id": "604g7bh4av2aj54114c14600",
                "role": "user"
            }
        },
        "resource": {
            "id": "/v1/user",
            "attributes": {
                "path": "/v1/user/604g7bh4av2aj54114c14600",
                "id": "604g7bh4av2aj54114c14600"
            }
        },
        "action": {
            "id": "",
            "attributes": {
                "method": "get"
            }
        },
        "context": {}
    },
]
# Parse JSON and create access request object
requests = [AccessRequest.from_json(request_json) for request_json in requests_json]

if __name__ == '__main__':
    # Check if access requests are allowed:

    # Edit of file by 604g7bh4av2aj54114c14600 --> Should be allowed.
    assert pdp.is_allowed(requests[0])
