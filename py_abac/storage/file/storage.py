"""
    File storage implementation
"""

import logging
import os
# shelve (and its pickle-based backing) is used here to persist policies in a
# local, operator-controlled file, not to deserialize untrusted external input.
import shelve  # nosec B403
from itertools import islice
from typing import Union, Generator

from ..base import Storage
from ...exceptions import PolicyExistsError
from ...policy import Policy

LOG = logging.getLogger(__name__)


class FileStorage(Storage):
    """
        Stores and retrieves policies from files on disk.

        .. important::

            This storage does not yet perform ACID transactions. It uses
            the python shelve package for storage which does not support
            transaction based access to stored objects. Thus so not use it
            in distributed applications. There is a separate project under
            development to address this issue.

        :param storage_dir: path to directory where storage files
            are to be saved.
    """
    # Policy storage file name
    POLICY_FILE = "policies"

    def __init__(self, storage_dir: str):
        # Create path directory if not exists
        os.makedirs(storage_dir, exist_ok=True)
        self._file = f"{os.path.abspath(storage_dir)}/{self.POLICY_FILE}"

    def add(self, policy: Policy):
        """
            Store a policy
        """
        with shelve.open(self._file, flag='c', writeback=True) as curr:  # nosec B301
            if policy.uid in curr:
                raise PolicyExistsError(policy.uid)
            curr[policy.uid] = policy.to_json()
        LOG.info('Added Policy: %s', policy)

    def get(self, uid: str) -> Union[Policy, None]:
        """
            Get specific policy
        """
        with shelve.open(self._file, flag='r') as curr:  # nosec B301
            policy_json = curr.get(uid, None)
            policy = Policy.from_json(policy_json) if policy_json else None
            return policy

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        """
            Retrieve all the policies within a window.

            .. note:

                Currently all policies are retrieved from storage and then
                sliced to given limit and offset. This issue will get resolved
                once indexing is supported for file storage.
        """
        self._check_limit_and_offset(limit, offset)
        with shelve.open(self._file, flag="r") as curr:  # nosec B301
            # Note: python by default sorts dict by key
            policies = islice(curr.values(), offset, offset + limit)
            for policy_json in policies:
                yield Policy.from_json(policy_json)

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        """
            Get all policies for given target IDs.

            .. note:

                Currently all policies are returned for evaluation.
        """
        # TODO: Create glob match based topologically sorted graph index for filtering  # pylint: disable=fixme
        with shelve.open(self._file, flag="r") as curr:  # nosec B301
            for policy_json in curr.values():
                yield Policy.from_json(policy_json)

    def update(self, policy: Policy):
        """
            Update a policy
        """
        with shelve.open(self._file, flag='c', writeback=True) as curr:  # nosec B301
            if policy.uid not in curr:
                raise ValueError(f"Policy with UID='{policy.uid}' does not exist.")
            curr[policy.uid] = policy.to_json()
        LOG.info('Updated Policy with UID=%s. New value is: %s', policy.uid, policy)

    def delete(self, uid: str):
        """
            Delete a policy
        """
        with shelve.open(self._file, flag='c', writeback=True) as curr:  # nosec B301
            if uid not in curr:
                raise ValueError(f"Policy with UID='{uid}' does not exist.")
            curr.pop(uid)
        LOG.info('Deleted Policy with UID=%s.', uid)
