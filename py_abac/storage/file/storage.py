"""
    File storage implementation
"""

import os
import shelve
import logging
import pathlib
from typing import Union, Generator

from ..base import Storage
from ...policy import Policy


class FileStorage(Storage):
    """
        Stores and retrieves policies from files on disk.

        .. important::

            This storage does not yet perform ACID transactions. Do not
            use it in multi-threaded or multiprocess setting.

        :param storage_dir: path to directory where storage files
            are to be saved.
    """
    # Policy storage file name
    POLICY_FILE = "policy"

    def __init__(self, storage_dir: str):
        # Create path directory if not exists
        os.makedirs(storage_dir, exist_ok=True)
        self._file = pathlib.Path(storage_dir) / self.POLICY_FILE

    def add(self, policy: Policy):
        with shelve.open(self._file, flag='c', writeback=True) as curr:
            curr[policy.uid] = policy.to_json()

    def get(self, uid: str) -> Union[Policy, None]:
        pass

    def get_all(self, limit: int, offset: int) -> Generator[Policy, None, None]:
        pass

    def get_for_target(
            self,
            subject_id: str,
            resource_id: str,
            action_id: str
    ) -> Generator[Policy, None, None]:
        pass

    def update(self, policy: Policy):
        pass

    def delete(self, uid: str):
        pass
