"""
    `EqualsAttribute` condition example.
"""

from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.memory import MemoryStorage

# Policy definition in JSON
policies_json = [
    {
        "uid": "1",
        "description": "Allow GET access to all members of team to which resource belongs.",
        "effect": "allow",
        "rules": {
            # Policy for all subjects
            "subject": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
            # Policy for when "owner.user" and "owner.team" attribute matches those in subject
            "resource": {
                "$.owner.team": {
                    "condition": "IsInAttribute",
                    "ace": "subject",
                    "path": "$.teams"
                }
            },
            # Policy for get action
            "action": {"$.method": {"condition": "Equals", "value": "get"}},
            "context": {}
        },
        "targets": {},
        "priority": 0
    },
    {
        "uid": "2",
        "description": "Allow GET, PUT and DELETE access to owning user of resource.",
        "effect": "allow",
        "rules": {
            # Policy for all subjects
            "subject": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
            # Policy for when "owner.user" and "owner.team" attribute matches those in subject
            "resource": {
                "$.owner.user": {
                    "condition": "EqualsAttribute",
                    "ace": "subject",
                    "path": "$.name"
                }
            },
            # Policy for get action
            "action": [{"$.method": {"condition": "Equals", "value": "get"}},
                       {"$.method": {"condition": "Equals", "value": "put"}},
                       {"$.method": {"condition": "Equals", "value": "delete"}}],
            "context": {}
        },
        "targets": {},
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
    # Edit of file by John --> Should be allowed.
    {
        "subject": {
            # User UUID
            "id": "urn::user::7f5bdcd7-97e9-42e2-a707-18429cba2617",
            "attributes": {
                "name": "John",
                "teams": ["Team A", "Team B"]
            }
        },
        "resource": {
            # File UUID
            "id": "urn::file::b56cebe6-bee6-45cc-9a26-d811a9140e56",
            "attributes": {
                "type": "file",
                "name": "Cooking Recipes",
                "owner": {
                    "user": "John",
                    "team": "Team A"
                }
            }
        },
        "action": {
            "id": "",
            "attributes": {"method": "put"}
        },
        "context": {}
    },
    # Read of file by Andrew --> Should be allowed since Andrew in part of Team A
    {
        "subject": {
            # User UUID
            "id": "urn::user::7f5bdcd7-97e9-42e2-a707-18429cba2617",
            "attributes": {
                "name": "Andrew",
                "teams": ["Team A"]
            }
        },
        "resource": {
            # File UUID
            "id": "urn::file::b56cebe6-bee6-45cc-9a26-d811a9140e56",
            "attributes": {
                "type": "file",
                "name": "Cooking Recipes",
                "owner": {
                    "user": "John",
                    "team": "Team A"
                }
            }
        },
        "action": {
            "id": "",
            "attributes": {"method": "get"}
        },
        "context": {}
    },
    # Edit of file by Andrew --> Should not be allowed since Andrew in not owner of file
    {
        "subject": {
            # User UUID
            "id": "urn::user::7f5bdcd7-97e9-42e2-a707-18429cba2617",
            "attributes": {
                "name": "Andrew",
                "teams": ["Team A"]
            }
        },
        "resource": {
            # File UUID
            "id": "urn::file::b56cebe6-bee6-45cc-9a26-d811a9140e56",
            "attributes": {
                "type": "file",
                "name": "Cooking Recipes",
                "owner": {
                    "user": "John",
                    "team": "Team A"
                }
            }
        },
        "action": {
            "id": "",
            "attributes": {"method": "put"}
        },
        "context": {}
    },
    # Read of file by Bob --> Should not be allowed since Bob in part of Team B
    {
        "subject": {
            # User UUID
            "id": "urn::user::7f5bdcd7-97e9-42e2-a707-18429cba2617",
            "attributes": {
                "name": "Bob",
                "teams": ["Team B"]
            }
        },
        "resource": {
            # File UUID
            "id": "urn::file::b56cebe6-bee6-45cc-9a26-d811a9140e56",
            "attributes": {
                "type": "file",
                "name": "Cooking Recipes",
                "owner": {
                    "user": "John",
                    "team": "Team A"
                }
            }
        },
        "action": {
            "id": "",
            "attributes": {"method": "get"}
        },
        "context": {}
    },
]
# Parse JSON and create access request object
requests = [AccessRequest.from_json(request_json) for request_json in requests_json]

if __name__ == '__main__':
    # Check if access requests are allowed:

    # Edit of file by John --> Should be allowed.
    assert pdp.is_allowed(requests[0])
    # Read of file by Andrew --> Should be allowed since Andrew in part of Team A
    assert pdp.is_allowed(requests[1])
    # Edit of file by Andrew --> Should not be allowed since Andrew in not owner of file
    assert not pdp.is_allowed(requests[2])
    # Read of file by Bob --> Should not be allowed since Bob in part of Team B
    assert not pdp.is_allowed(requests[3])
