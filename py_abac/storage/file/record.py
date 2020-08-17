"""
    Record storage

    This file contains implementation for storing variable sized chunks
    of data called records in an underlying block storage.
"""

import logging

from .block import BlockStorage

LOG = logging.getLogger(__name__)


class RecordStorage:
    """
        Record Storage Class

        Saves variable length data records in a block storage. Each record
        is a string value saved in one or more blocks in a file.

        :param storage: block storage instance.
    """

    def __init__(self, storage: BlockStorage):
        self._storage = storage

    def add(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
