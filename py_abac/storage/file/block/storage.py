"""
    Block Storage

    This file contains implementation for storing data in files as fixed
    size blocks.
"""

import json
import logging
from typing import Union, List

from .block import Block
from .utility import save_at, load_from

LOG = logging.getLogger(__name__)

DEFAULT_BLOCK_SIZE = 4096


class MetaData:
    """
        Block storage metadata.

        :param block_size: size of individual block
        :param total_blocks: total number of blocks in file
        :param free_blocks: number of free blocks
    """
    # Offset to the first block
    offset: int = 128
    # Storage format version
    version: str = "0.1"

    def __init__(
            self,
            block_size: int,
            total_blocks: int = 0,
            free_blocks: List[int] = None,
            *_, **__
    ):
        self._block_size: int = block_size
        self._total_blocks: int = total_blocks
        self._free_blocks: List[int] = free_blocks or []

    @property
    def block_size(self) -> int:
        return self._block_size

    @property
    def free_blocks(self) -> List[int]:
        return self._free_blocks

    @free_blocks.setter
    def free_blocks(self, value: int):
        self._free_blocks = value

    @property
    def total_blocks(self) -> int:
        return self._total_blocks

    @total_blocks.setter
    def total_blocks(self, value: int):
        self._total_blocks = value

    @classmethod
    def load(cls, fd: "TextIO") -> "MetaData":
        """
            Load and deserialize metadata object from a storage file.

            :param fd: file descriptor
            :returns: MetaData object
        """
        # Loading part 1 of the metadata
        metadata_part_1_str = load_from(fd, 0, cls.offset)
        metadata_part_1_dict = json.loads(metadata_part_1_str)

        # TODO: Loading part 2 of the metadata

        metadata_dict = {**metadata_part_1_dict}

        return cls(**metadata_dict)

    def dump(self, fd: "TextIO"):
        """
            Dump serialized metadata object into a storage file.

            :param fd: file descriptor
        """
        # TODO: Save part 2 of the metadata

        # Saving part 1 of the metadata
        metadata_part_1_dict = {
            "block_size": self.block_size,
            "version": self.version
        }
        metadata_part_1_str = json.dumps(metadata_part_1_dict)
        save_at(fd, metadata_part_1_str, 0)


class BlockStorage:
    """
        Block Storage Class.

        Saves raw data as fixed sized blocks in a file.

        :param file_name: file path where data is stored.
        :param block_size: size of an individual block. Defaults to 4KB.
    """

    def __init__(self, file_name: str, block_size: int = DEFAULT_BLOCK_SIZE):
        self._file_name = file_name
        self._block_size = block_size
        self._metadata: Union[MetaData, None] = None

    def __enter__(self):
        """
            Context manager entry
        """
        self._fd = open(self._file_name, "w+")
        self._metadata = MetaData.load(self._fd)
        if not self._metadata:
            self._metadata = MetaData(self._block_size)
            self._metadata.dump(self._fd)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Context manager exit
        """
        self._fd.close()

    def read(self, block_id: int) -> str:
        """
            Read stored data at given block ID. An error will be
            thrown if the stored data extends multiple blocks and
            the given ID is not the starting block.

            :param block_id: block ID from where to start reading
            :returns: stored contents in one or more linked blocks
        """

    def write(self, string: str, block_id: int = None) -> List[Block]:
        """
            Write the given string in the block storage. Optionally
            the block ID where the data should be stored can also be
            specified.

            :param string: data string to store
            :param block_id: block ID where the string should be
                written. If set to None then new blocks will be
                created to insert the string. Otherwise the original
                data will be overwritten. An error will be thrown in
                case the original data extends multiple blocks and the
                given ID is not the starting block.
            :returns: list of blocks in which the string is stored
        """

    def _save(self, blocks: List[Block]):
        """
            Persist given list of blocks in opened file on disk.
        """

    def _create(self) -> Block:
        """
            Creates a new empty block and updates the metadata.

            :returns: Newly created block object
        """
        self._metadata.total_blocks += 1
        self._metadata.free_blocks += 1
        return Block(self._metadata.total_blocks)
