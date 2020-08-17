"""
    Utility methods
"""


def save_at(fd: "TextIO", data: str, offset: int):
    """
        Save data at certain location in file.

        :param fd: file descriptor to use for writing
        :param data: data to save
        :param offset: offset location to read from
    """
    # Get current file cursor offset
    curr_offset = fd.tell()
    # Set cursor to given offset
    fd.seek(offset)
    # Save data
    fd.write(data)
    # Set cursor pointer to original offset
    fd.seek(curr_offset)


def load_from(fd, offset: int, num: int) -> str:
    """
        Load data from certain offset and given size from a file.

        :param fd: file descriptor to use for reading
        :param offset: offset location to read from
        :param num: number of bytes to read
        :returns: returns loaded data
    """
    # Get current file cursor offset
    curr_offset = fd.tell()
    # Set cursor to given offset
    fd.seek(offset)
    # Read specified number of bytes
    data = fd.read(num)
    # Set cursor pointer to original offset
    fd.seek(curr_offset)

    return data
