"""
Version for pyabac package
"""

__version__ = '0.2.0'


def version_info():
    """
    Get version of pyabac package as tuple
    """
    return tuple(map(int, __version__.split('.')))
