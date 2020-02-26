"""
Version for py_abac package
"""

__version__ = '0.2.1'  # pragma: no cover


def version_info():  # pragma: no cover
    """
    Get version of py_abac package as tuple
    """
    return tuple(map(int, __version__.split('.')))  # pragma: no cover
