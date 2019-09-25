"""
    Policy tests
"""

import pytest

from pyabac.conditions.logic import OrCondition
from pyabac.conditions.net import CIDRCondition
from pyabac.conditions.numeric import GreaterCondition
from pyabac.conditions.string import EqualsCondition
from pyabac.inquiry import Inquiry
from pyabac.policy import Policy


class TestPolicy(object):

    @pytest.mark.parametrize("policy, inquiry, result", [
        (Policy(subjects=[{"name": EqualsCondition("admin")}]),
         Inquiry(subject={"name": "admin"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin")}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": EqualsCondition("GET")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         True),
        (Policy(subjects=[{"name": EqualsCondition("john")}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": EqualsCondition("GET")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin"), "age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": EqualsCondition("GET")}]),
         Inquiry(subject={"name": "admin"},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin"), "age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": EqualsCondition("GET")}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin"), "age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": EqualsCondition("GET")}]),
         Inquiry(subject={"name": "admin", "age": 40},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         True),
        (Policy(subjects=[{"name": EqualsCondition("admin")}, {"age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": EqualsCondition("GET")}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "GET"}),
         True),
        (Policy(subjects=[{"name": EqualsCondition("admin")}, {"age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": EqualsCondition("GET")}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin")}, {"age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": OrCondition(EqualsCondition("GET"), EqualsCondition("PUT"))}]),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"}),
         True),
        (Policy(subjects=[{"name": EqualsCondition("admin")}, {"age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": OrCondition(EqualsCondition("GET"), EqualsCondition("PUT"))}],
                context={"ip": CIDRCondition("127.0.0.0/24")}),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin")}, {"age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": OrCondition(EqualsCondition("GET"), EqualsCondition("PUT"))}],
                context={"ip": CIDRCondition("127.0.0.0/24")}),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"},
                 context={"ip": "192.168.1.100"}),
         False),
        (Policy(subjects=[{"name": EqualsCondition("admin")}, {"age": GreaterCondition(30)}],
                resources=[{"url": EqualsCondition("/api/v1/health")}],
                actions=[{"method": OrCondition(EqualsCondition("GET"), EqualsCondition("PUT"))}],
                context={"ip": CIDRCondition("127.0.0.0/24")}),
         Inquiry(subject={"name": "admin", "age": 20},
                 resource={"url": "/api/v1/health"},
                 action={"method": "PUT"},
                 context={"ip": "127.0.0.10"}),
         True),
    ])
    def test_fits(self, policy, inquiry, result, benchmark):
        fits = benchmark(policy.fits, inquiry)
        assert fits == result


if __name__ == '__main__':
    pytest.main()
