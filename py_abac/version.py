"""
Version for py_abac package
"""

__version__ = '0.1.1'


def version_info():
    """
    Get version of py_abac package as tuple
    """
    return tuple(map(int, __version__.split('.')))
