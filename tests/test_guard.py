"""
    Guard tests
"""

import pytest

from pyabac.constants import DENY_ACCESS, ALLOW_ACCESS
from pyabac.guard import Guard
from pyabac.inquiry import Inquiry
from pyabac.policy import Policy
from pyabac.conditions.exists import ExistsCondition
from pyabac.conditions.logic import OrCondition
from pyabac.conditions.net import CIDRCondition
from pyabac.conditions.string import EqualsCondition, RegexMatchCondition
from pyabac.storage.memory import MemoryStorage

st = MemoryStorage()
policies = [
    Policy(
        uid='1',
        description="""
        Max, Nina, Ben, Henry are allowed to create, delete, get the resources
        only if the client IP matches.
        """,
        effect=ALLOW_ACCESS,
        subjects=[{"name": EqualsCondition('Max')},
                  {"name": EqualsCondition('Nina')},
                  {"name": OrCondition(EqualsCondition('Ben'), EqualsCondition('Henry'))}],
        resources=[{"name": OrCondition(
            EqualsCondition('myrn:example.com:resource:123'),
            EqualsCondition('myrn:example.com:resource:345'),
            RegexMatchCondition('myrn:something:foo:.*'))}],
        actions=[{"method": OrCondition(EqualsCondition('create'), EqualsCondition('delete'))},
                 {"method": EqualsCondition('get')}],
        context={'ip': CIDRCondition('127.0.0.1/32')},
    ),
    Policy(
        uid='2',
        description='Allows Max to update any resource',
        effect=ALLOW_ACCESS,
        subjects=[{"name": EqualsCondition('Max')}],
        actions=[{"method": EqualsCondition('update')}],
        resources=[{"name": RegexMatchCondition('.*')}],
    ),
    Policy(
        uid='3',
        description='Max is not allowed to print any resource',
        effect=DENY_ACCESS,
        subjects=[{"name": EqualsCondition('Max')}],
        actions=[{"method": EqualsCondition('print')}],
        resources=[{"name": RegexMatchCondition('.*')}],
    ),
    Policy(
        uid='4'
    ),
    Policy(
        uid='5',
        description='Allows Nina to update any resources that have only digits',
        effect=ALLOW_ACCESS,
        subjects=[{"name": EqualsCondition('Nina')}],
        actions=[{"method": EqualsCondition('update')}],
        resources=[{"name": RegexMatchCondition(r'\d+')}],
    ),
    Policy(
        uid='6',
        description='Allows Nina to update any resources that have only digits.',
        effect=ALLOW_ACCESS,
        subjects=[{"name": EqualsCondition('Nina')}],
        actions=[{"method": EqualsCondition('update')}, {"method": EqualsCondition('read')}],
        resources=[{'id': RegexMatchCondition(r'\d+'), 'magazine': RegexMatchCondition(r'[\d\w]+')}],
    ),
    Policy(
        uid='7',
        description='Prevent Nina to update any resources when ID is passed in context',
        effect=DENY_ACCESS,
        subjects=[{"name": EqualsCondition('Nina')}],
        actions=[{"method": EqualsCondition('update')}, {"method": EqualsCondition('read')}],
        resources=[{'id': RegexMatchCondition(r'\d+'), 'magazine': RegexMatchCondition(r'[\d\w]+')}],
        context={'id': ExistsCondition()}
    ),
]
for policy in policies:
    st.add(policy)


@pytest.mark.parametrize('desc, inquiry, should_be_allowed', [
    (
            'Empty inquiry carries no information, so nothing is allowed, even empty Policy #4',
            Inquiry(),
            False,
    ),
    (
            'Max is allowed to update anything',
            Inquiry(
                subject={'name': 'Max'},
                resource={'name': 'myrn:example.com:resource:123'},
                action={'method': 'update'}
            ),
            True,
    ),
    (
            'Max is allowed to update anything, even empty one',
            Inquiry(
                subject={'name': 'Max'},
                resource={'name': ''},
                action={'method': 'update'}
            ),
            True,
    ),
    (
            'Max, but not max is allowed to update anything (case-sensitive comparison)',
            Inquiry(
                subject={'name': 'max'},
                resource={'name': 'myrn:example.com:resource:123'},
                action={'method': 'update'}
            ),
            False,
    ),
    (
            'Max is not allowed to print anything',
            Inquiry(
                subject={'name': 'Max'},
                resource={'name': 'myrn:example.com:resource:123'},
                action={'method': 'print'},
            ),
            False,
    ),
    (
            'Max is not allowed to print anything, even if no resource is given',
            Inquiry(
                subject={'name': 'Max'},
                action={'method': 'print'}
            ),
            False,
    ),
    (
            'Max is not allowed to print anything, even an empty resource',
            Inquiry(
                subject={'name': 'Max'},
                action={'method': 'print'},
                resource={'name': ''}
            ),
            False,
    ),
    (
            'Policy #1 matches and has allow-effect',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'ip': '127.0.0.1'}
            ),
            True,
    ),
    (
            'Policy #1 matches - Henry is listed in the allowed subjects regexp',
            Inquiry(
                subject={'name': 'Henry'},
                action={'method': 'get'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'ip': '127.0.0.1'}
            ),
            True,
    ),
    (
            'Policy #1 does not match - context was not found (misspelled)',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'IP': '127.0.0.1'}
            ),
            False,
    ),
    (
            'Policy #1 does not match - context is missing',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={}
            ),
            False,
    ),
    (
            'Policy #1 does not match - context says IP is not in the allowed range',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'delete'},
                resource={'name': 'myrn:example.com:resource:123'},
                context={'ip': '0.0.0.0'}
            ),
            False,
    ),
    (
            'Policy #5 does not match - action is update, but subjects does not match',
            Inquiry(
                subject={'name': 'Sarah'},
                action={'method': 'update'},
                resource={'name': '88'},
            ),
            False,
    ),
    (
            'Policy #5 does not match - action is update, subject is Nina, but resource-name is not digits',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'update'},
                resource={'name': 'abcd'},
            ),
            False,
    ),
    (
            'Policy #6 does not match - Inquiry has wrong format for resource',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'update'},
                resource={'name': 'abcd'},
            ),
            False,
    ),
    (
            'Policy #6 does not match - Inquiry has string ID for resource',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': 'abcd'},
            ),
            False,
    ),
    (
            'Policy #6 should match',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'update'},
                resource={'id': '00678', 'magazine': 'Playboy1'},
            ),
            True,
    ),
    (
            'Policy #6 should not match - usage of inappropriate resource ID',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': 'abc', 'magazine': 'Playboy1'},
            ),
            False,
    ),
    (
            'Policy #7 should match - usage of inappropriate context',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': '00678', 'magazine': 'Playboy1'},
                context={'id': 'Nina'}
            ),
            False,
    ),
    (
            'Policy #7 should not match - usage of different context',
            Inquiry(
                subject={'name': 'Nina'},
                action={'method': 'read'},
                resource={'id': '00678', 'magazine': 'Playboy1'},
                context={'name': 'Nina'}
            ),
            True,
    ),
])
def test_is_allowed(desc, inquiry, should_be_allowed):
    g = Guard(st)
    assert should_be_allowed == g.is_allowed(inquiry)


def test_guard_create_error():
    with pytest.raises(TypeError):
        Guard(None)


def test_is_allowed_error():
    g = Guard(st)
    with pytest.raises(TypeError):
        g.is_allowed(None)
