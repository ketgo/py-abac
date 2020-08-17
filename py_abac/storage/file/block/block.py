"""
    Block Unit

    A unit size of storage in file.
"""

import json
from typing import Union


class Block:
    """
        Block of fixed size in a file.

        :param id: unique ID of the block
    """

    def __init__(self, id: int):
        # Unique ID of the block
        self._id = id
        # Stored content size
        self._cs: int = 0
        # Linked next block ID
        self._nb_id: Union[int, None] = None
        # Linked previous block ID
        self._pb_id: Union[int, None] = None
        # Stored content
        self._content: str = ""

    @property
    def id(self) -> int:
        return self._id

    @property
    def content_size(self) -> int:
        """
            Number of bytes in the content of the block. This does
            not include the header size of the block.
        """
        return self._cs

    @property
    def next_block_id(self) -> Union[int, None]:
        """
            ID of next block which contains rest of the parts of the
            stored incomplete record in this block.
        """
        return self._nb_id

    @next_block_id.setter
    def next_block_id(self, value: int):
        self._nb_id = value

    @property
    def prev_block_id(self) -> Union[int, None]:
        """
            ID of previous block which contains rest of the parts of the
            stored incomplete record in this block.
        """
        return self._pb_id

    @prev_block_id.setter
    def prev_block_id(self, value: int):
        self._pb_id = value

    @property
    def content(self) -> str:
        """
            Content stored in the block. This does not include
            header information.
        """
        return self._content

    @content.setter
    def content(self, value: str):
        self._content = value
        self._cs = len(self._content)

    @property
    def is_root(self) -> bool:
        """
            Check if this is a root block.
        """
        return self._pb_id is None

    @property
    def header_size(self) -> int:
        """
            Size of the block headers.
        """
        block_dict = self.__dict__.copy()
        block_dict["_content"] = ""
        block_str = json.dumps(block_dict)
        return len(block_str)

    @classmethod
    def loads(cls, string: str) -> "Block":
        """
            Deserialize block object from string.

            :param string: string to parse
            :returns: Block object
        """
        block_dict = json.loads(string)
        return cls(**block_dict)

    @staticmethod
    def dumps(block: "Block") -> str:
        """
            Serialize block object into string.

            :param block: block object to serialize
            :returns: serialized block
        """
        block_dict = block.__dict__
        return json.dumps(block_dict)
