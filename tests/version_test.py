from copy import copy

import pytest

from pep440_version_utils import Version

test_versions_for_copy = [
    "1.0.0",
    "1.0.0.dev1",
]

@pytest.mark.parametrize("version_string", test_versions_for_copy)
def test_copy(version_string):
    version1 = Version("1.0.0")
    version2 = copy(version1)

    assert version1 == version2
    assert version1 is not version2
    assert version1._version == version2._version
    assert version1._version is not version2._version
    assert version1._key == version2._key
    assert version1._key is not version2._key


test_versions_for_next_major = [
    ("0.0.1", "1.0.0"),
    ("0.1.1", "1.0.0"),
    ("1.1.1", "2.0.0"),
    ("1.1.1a1", "2.0.0"),
    ("1.1.0b10", "2.0.0"),
    ("2.0.0a1", "2.0.0"),
    ("2.0.0rc2", "2.0.0"),
    ("2.0.0b4", "2.0.0"),
    ("2.0.0b4.post1", "2.0.0"),
    ("1.1.1.dev1", "2.0.0"),
    ("1.1.0.dev2", "2.0.0"),
    ("2.0.0.dev10", "2.0.0"),
    ("1.1.1a1.dev1", "2.0.0"),
    ("1.1.0b10.dev1", "2.0.0"),
    ("2.0.0a1.dev1", "2.0.0"),
    ("2.0.0rc2.dev1", "2.0.0"),
    ("2.0.0b4.dev1", "2.0.0"),
    ("2.0.0b4.post1.dev1", "2.0.0"),
]


@pytest.mark.parametrize(
    "version_string,expected", test_versions_for_next_major
)
def test_next_major(version_string, expected):
    version = Version(version_string)
    next_version = version.next_major()
    assert isinstance(next_version, Version)
    assert next_version > version
    assert str(next_version) == expected


test_versions_for_next_minor = [
    ("0.0.1", "0.1.0"),
    ("0.1.1", "0.2.0"),
    ("1.1.1", "1.2.0"),
    ("1.1.1a1", "1.2.0"),
    ("1.2.0a1", "1.2.0"),
    ("1.2.0rc2", "1.2.0"),
    ("1.2.0b4", "1.2.0"),
    ("1.2.0b4.post1", "1.2.0"),
    ("1.1.1.dev1", "1.2.0"),
    ("1.2.0.dev2", "1.2.0"),
    ("1.2.0.dev10", "1.2.0"),
    ("1.1.1a1.dev1", "1.2.0"),
    ("1.2.0a1.dev1", "1.2.0"),
    ("1.2.0rc2.dev1", "1.2.0"),
    ("1.2.0b4.dev1", "1.2.0"),
    ("1.2.0b4.post1.dev1", "1.2.0"),
]


@pytest.mark.parametrize(
    "version_string,expected", test_versions_for_next_minor
)
def test_next_minor(version_string, expected):
    version = Version(version_string)
    next_version = version.next_minor()
    assert isinstance(next_version, Version)
    assert next_version > version
    assert str(next_version) == expected


test_versions_for_next_micro = [
    ("0.0.1", "0.0.2"),
    ("0.1.1", "0.1.2"),
    ("1.1.1", "1.1.2"),
    ("1.2.1a1", "1.2.1"),
    ("1.2.2a1", "1.2.2"),
    ("1.2.0a1", "1.2.1"),
    ("1.2.0rc2", "1.2.1"),
    ("1.2.0b4", "1.2.1"),
    ("1.2.0b4.post1", "1.2.1"),
    ("1.2.1.dev1", "1.2.1"),
    ("1.2.2.dev2", "1.2.2"),
    ("1.2.0.dev10", "1.2.1"),
    ("1.2.1a1.dev1", "1.2.1"),
    ("1.2.2a1.dev1", "1.2.2"),
    ("1.2.0a1.dev1", "1.2.1"),
    ("1.2.0rc2.dev1", "1.2.1"),
    ("1.2.0b4.dev1", "1.2.1"),
    ("1.2.0b4.post1.dev1", "1.2.1"),
]


@pytest.mark.parametrize(
    "version_string,expected", test_versions_for_next_micro
)
def test_next_micro(version_string, expected):
    version = Version(version_string)
    next_version = version.next_micro()
    assert isinstance(next_version, Version)
    assert next_version > version
    assert str(next_version) == expected


test_versions_for_next_alpha = [
    ("0.0.1", "micro", "0.0.2a1"),
    ("0.0.1", "minor", "0.1.0a1"),
    ("0.0.1", "major", "1.0.0a1"),
    ("0.1.1", "micro", "0.1.2a1"),
    ("0.1.1", "minor", "0.2.0a1"),
    ("0.1.1", "major", "1.0.0a1"),
    ("1.1.1", "micro", "1.1.2a1"),
    ("1.1.1", "minor", "1.2.0a1"),
    ("1.1.1", "major", "2.0.0a1"),
    ("1.2.1a1", "micro", "1.2.1a2"),
    ("1.2.1a1", "minor", "1.2.1a2"),
    ("1.2.1a1", "major", "1.2.1a2"),
    ("0.0.1.dev1", "micro", "0.0.1a1"),
    ("0.0.1.dev1", "minor", "0.0.1a1"),
    ("0.0.1.dev1", "major", "0.0.1a1"),
    ("0.1.1.dev1", "micro", "0.1.1a1"),
    ("0.1.1.dev1", "minor", "0.1.1a1"),
    ("0.1.1.dev1", "major", "0.1.1a1"),
    ("1.1.1.dev1", "micro", "1.1.1a1"),
    ("1.1.1.dev1", "minor", "1.1.1a1"),
    ("1.1.1.dev1", "major", "1.1.1a1"),
    ("1.2.1a2.dev1", "micro", "1.2.1a2"),
    ("1.2.1a2.dev1", "minor", "1.2.1a2"),
    ("1.2.1a2.dev1", "major", "1.2.1a2"),
]


@pytest.mark.parametrize(
    "version_string,version_bump,expected", test_versions_for_next_alpha,
)
def test_next_alpha(version_string, version_bump, expected):
    version = Version(version_string)
    next_version = version.next_alpha(version_bump)
    assert isinstance(next_version, Version)
    assert next_version > version
    assert str(next_version) == expected


test_versions_for_next_beta = [
    ("0.0.1", "micro", "0.0.2b1"),
    ("0.0.1", "minor", "0.1.0b1"),
    ("0.0.1", "major", "1.0.0b1"),
    ("0.1.1", "micro", "0.1.2b1"),
    ("0.1.1", "minor", "0.2.0b1"),
    ("0.1.1", "major", "1.0.0b1"),
    ("1.1.1", "micro", "1.1.2b1"),
    ("1.1.1", "minor", "1.2.0b1"),
    ("1.1.1", "major", "2.0.0b1"),
    ("1.2.1a1", "micro", "1.2.1b1"),
    ("1.2.1a1", "minor", "1.2.1b1"),
    ("1.2.1a1", "major", "1.2.1b1"),
    ("1.2.1b1", "micro", "1.2.1b2"),
    ("1.2.1b1", "minor", "1.2.1b2"),
    ("1.2.1b1", "major", "1.2.1b2"),
    ("0.0.1.dev1", "micro", "0.0.1b1"),
    ("0.0.1.dev1", "minor", "0.0.1b1"),
    ("0.0.1.dev1", "major", "0.0.1b1"),
    ("0.1.1.dev1", "micro", "0.1.1b1"),
    ("0.1.1.dev1", "minor", "0.1.1b1"),
    ("0.1.1.dev1", "major", "0.1.1b1"),
    ("1.1.1.dev1", "micro", "1.1.1b1"),
    ("1.1.1.dev1", "minor", "1.1.1b1"),
    ("1.1.1.dev1", "major", "1.1.1b1"),
    ("1.2.1a2.dev1", "micro", "1.2.1b1"),
    ("1.2.1a2.dev1", "minor", "1.2.1b1"),
    ("1.2.1a2.dev1", "major", "1.2.1b1"),
    ("1.2.1b2.dev1", "micro", "1.2.1b2"),
    ("1.2.1b2.dev1", "minor", "1.2.1b2"),
    ("1.2.1b2.dev1", "major", "1.2.1b2"),
]


@pytest.mark.parametrize(
    "version_string,version_bump,expected", test_versions_for_next_beta,
)
def test_next_beta(version_string, version_bump, expected):
    version = Version(version_string)
    next_version = version.next_beta(version_bump)
    assert isinstance(next_version, Version)
    assert next_version > version
    assert str(next_version) == expected


test_versions_for_next_release_candidate = [
    ("0.0.1", "micro", "0.0.2rc1"),
    ("0.0.1", "minor", "0.1.0rc1"),
    ("0.0.1", "major", "1.0.0rc1"),
    ("0.1.1", "micro", "0.1.2rc1"),
    ("0.1.1", "minor", "0.2.0rc1"),
    ("0.1.1", "major", "1.0.0rc1"),
    ("1.1.1", "micro", "1.1.2rc1"),
    ("1.1.1", "minor", "1.2.0rc1"),
    ("1.1.1", "major", "2.0.0rc1"),
    ("1.2.1a1", "micro", "1.2.1rc1"),
    ("1.2.1a1", "minor", "1.2.1rc1"),
    ("1.2.1a1", "major", "1.2.1rc1"),
    ("1.2.1b1", "micro", "1.2.1rc1"),
    ("1.2.1b1", "minor", "1.2.1rc1"),
    ("1.2.1b1", "major", "1.2.1rc1"),
    ("1.2.1rc1", "micro", "1.2.1rc2"),
    ("1.2.1rc1", "minor", "1.2.1rc2"),
    ("1.2.1rc1", "major", "1.2.1rc2"),
    ("0.0.1.dev1", "micro", "0.0.1rc1"),
    ("0.0.1.dev1", "minor", "0.0.1rc1"),
    ("0.0.1.dev1", "major", "0.0.1rc1"),
    ("0.1.1.dev1", "micro", "0.1.1rc1"),
    ("0.1.1.dev1", "minor", "0.1.1rc1"),
    ("0.1.1.dev1", "major", "0.1.1rc1"),
    ("1.1.1.dev1", "micro", "1.1.1rc1"),
    ("1.1.1.dev1", "minor", "1.1.1rc1"),
    ("1.1.1.dev1", "major", "1.1.1rc1"),
    ("1.2.1a2.dev1", "micro", "1.2.1rc1"),
    ("1.2.1a2.dev1", "minor", "1.2.1rc1"),
    ("1.2.1a2.dev1", "major", "1.2.1rc1"),
    ("1.2.1b2.dev1", "micro", "1.2.1rc1"),
    ("1.2.1b2.dev1", "minor", "1.2.1rc1"),
    ("1.2.1b2.dev1", "major", "1.2.1rc1"),
    ("1.2.1rc2.dev1", "micro", "1.2.1rc2"),
    ("1.2.1rc2.dev1", "minor", "1.2.1rc2"),
    ("1.2.1rc2.dev1", "major", "1.2.1rc2"),
]


@pytest.mark.parametrize(
    "version_string,version_bump,expected",
    test_versions_for_next_release_candidate,
)
def test_next_release_candidate(
    version_string,
    version_bump,
    expected
):
    version = Version(version_string)
    next_version = version.next_release_candidate(version_bump)
    assert isinstance(next_version, Version)
    assert next_version > version
    assert str(next_version) == expected

test_versions_for_next_dev = [
    ("0.0.1", "micro", "0.0.2.dev1"),
    ("0.0.1", "minor", "0.1.0.dev1"),
    ("0.0.1", "major", "1.0.0.dev1"),
    ("0.1.1", "micro", "0.1.2.dev1"),
    ("0.1.1", "minor", "0.2.0.dev1"),
    ("0.1.1", "major", "1.0.0.dev1"),
    ("1.1.1", "micro", "1.1.2.dev1"),
    ("1.1.1", "minor", "1.2.0.dev1"),
    ("1.1.1", "major", "2.0.0.dev1"),
    ("1.2.1a1", "micro", "1.2.1a2.dev1"),
    ("1.2.1a1", "minor", "1.2.1a2.dev1"),
    ("1.2.1a1", "major", "1.2.1a2.dev1"),
    ("1.2.1b1", "micro", "1.2.1b2.dev1"),
    ("1.2.1b1", "minor", "1.2.1b2.dev1"),
    ("1.2.1b1", "major", "1.2.1b2.dev1"),
    ("1.2.1rc1", "micro", "1.2.1rc2.dev1"),
    ("1.2.1rc1", "minor", "1.2.1rc2.dev1"),
    ("1.2.1rc1", "major", "1.2.1rc2.dev1"),
    ("1.2.1.dev1", "micro", "1.2.1.dev2"),
    ("1.2.1.dev1", "minor", "1.2.1.dev2"),
    ("1.2.1.dev1", "major", "1.2.1.dev2"),
    ("1.2.1a1.dev1", "micro", "1.2.1a1.dev2"),
    ("1.2.1a1.dev1", "minor", "1.2.1a1.dev2"),
    ("1.2.1a1.dev1", "major", "1.2.1a1.dev2"),
    ("1.2.1b1.dev1", "micro", "1.2.1b1.dev2"),
    ("1.2.1b1.dev1", "minor", "1.2.1b1.dev2"),
    ("1.2.1b1.dev1", "major", "1.2.1b1.dev2"),
    ("1.2.1rc1.dev1", "micro", "1.2.1rc1.dev2"),
    ("1.2.1rc1.dev1", "minor", "1.2.1rc1.dev2"),
    ("1.2.1rc1.dev1", "major", "1.2.1rc1.dev2"),
]


@pytest.mark.parametrize(
    "version_string,version_bump,expected", test_versions_for_next_dev,
)
def test_next_dev(version_string, version_bump, expected):
    version = Version(version_string)
    next_version = version.next_dev(version_bump)
    assert isinstance(next_version, Version)
    assert next_version > version
    assert str(next_version) == expected


def test_next_prerelease_invalid():
    version = Version("1.1.1")
    with pytest.raises(TypeError):
        version.next_alpha("stuff")

    with pytest.raises(TypeError):
        version.next_beta("stuff")

    with pytest.raises(TypeError):
        version.next_release_candidate("stuff")


test_versions_is_alpha = [
    ("0.0.1", False),
    ("1.2.1a1", True),
    ("1.2.1b1", False),
    ("1.2.1rc1", False),
]


@pytest.mark.parametrize(
    "version_string,expected", test_versions_is_alpha,
)
def test_is_alpha(version_string, expected):
    version = Version(version_string)
    assert version.is_alpha is expected


test_versions_is_beta = [
    ("0.0.1", False),
    ("1.2.1a1", False),
    ("1.2.1b1", True),
    ("1.2.1rc1", False),
]


@pytest.mark.parametrize(
    "version_string,expected", test_versions_is_beta,
)
def test_is_beta(version_string, expected):
    version = Version(version_string)
    assert version.is_beta is expected


test_versions_is_release_candidate = [
    ("0.0.1", False),
    ("1.2.1a1", False),
    ("1.2.1b1", False),
    ("1.2.1rc1", True),
]


@pytest.mark.parametrize(
    "version_string,expected", test_versions_is_release_candidate,
)
def test_is_release_candidate(version_string, expected):
    version = Version(version_string)
    assert version.is_release_candidate is expected
