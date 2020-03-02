"""
    SQL Storage implementation
"""

import logging
from typing import Union, Generator

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from .model import PolicyModel
from ..base import StorageBase
from ...exceptions import PolicyExistsError
from ...policy import Policy

LOG = logging.getLogger(__name__)


class SQLStorage(StorageBase):
    """
        Stores and retrieves policies from SQL database

        :param scoped_session: SQL Alchemy scoped session
    """

    def __init__(self, scoped_session):
        self.session = scoped_session
        self.dialect = scoped_session.bind.engine.dialect.name

    def add(self, policy: Policy):
        try:
            policy_model = PolicyModel.from_policy(policy)
            self.session.add(policy_model)
            self.session.commit()
            LOG.info("Added Policy: %s", policy)
        except (IntegrityError, FlushError):
            self.session.rollback()
            LOG.error("Error trying to create already existing policy with UID=%s.", policy.uid)
            raise PolicyExistsError(policy.uid)

    def get(self, uid: str) -> Union[Policy, None]:
        policy_model = self.session.query(PolicyModel).get(uid)
        return policy_model.to_policy() if policy_model else None

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        self._check_limit_and_offset(limit, offset)
        cur = self.session.query(PolicyModel).order_by(PolicyModel.uid.asc()) \
            .slice(offset, offset + limit)
        for policy_model in cur:
            yield policy_model.to_policy()

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        policy_filter = PolicyModel.get_filter(subject_id, resource_id, action_id)
        cur = self.session.query(PolicyModel).filter(*policy_filter)
        for policy_model in cur:
            yield policy_model.to_policy()

    def update(self, policy: Policy):
        try:
            policy_model = self.session.query(PolicyModel).get(policy.uid)
            if not policy_model:
                return
            policy_model.update(policy)
            self.session.commit()
        except IntegrityError:  # pragma: no cover
            self.session.rollback()  # pragma: no cover
            raise  # pragma: no cover
        LOG.info('Updated Policy with UID=%s. New value is: %s', policy.uid, policy)

    def delete(self, uid: str):
        self.session.query(PolicyModel).filter(PolicyModel.uid == uid).delete()
        LOG.info("Deleted Policy with UID=%s.", uid)
