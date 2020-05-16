import pytest

from pep440_version_utils import is_valid_version

test_versions = (
    ("0.9", True),
    ("0.9.1", True),
    ("0.9.2", True),
    ("0.9.10", True),
    ("0.9.11", True),
    ("1.0", True),
    ("1.0.1", True),
    ("1.1", True),
    ("2.0", True),
    ("2.0.1", True),
    ("1.2a1", True),
    ("2.1b2", True),
    ("2.0rc1", True),
    ("1.1.post1", True),
    ("1.1a2.post32", True),
    ("1.1b3.post1", True),
    ("1.1rc2.post2", True),
    ("3.4a1.dev1", True),
    ("3.4b2.dev1", True),
    ("3.4rc1.dev1", True),
    ("3.4.post4.dev1", True),
    ("2012.4", True),
    ("2012.7", True),
    ("2012.10", True),
    ("2013.1", True),
    ("2013.6", True),
    # invalid
    ("foobar", False),
)


@pytest.mark.parametrize("version,expected", test_versions)
def test_is_valid_version(version, expected):
    assert is_valid_version(version) is expected
