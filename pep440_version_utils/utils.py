from typing import Text

from packaging.version import InvalidVersion

from .version import Version


def is_valid_version(version_string: Text) -> bool:
    """
    Return True if a version strictly follows PEP440.
    """
    try:
        Version(version_string)
    except InvalidVersion:
        return False
    return True
