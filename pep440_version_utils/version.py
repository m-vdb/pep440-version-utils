from copy import copy
from typing import Optional, Tuple, Text

from packaging.version import (
    Version as BaseVersion,
    _Version as VersionNamedTuple,
    _cmpkey,
)


ALPHA_SEGMENT = "a"
BETA_SEGMENT = "b"
RC_SEGMENT = "rc"


class Version(BaseVersion):
    """
    Supercede `packaging.version.Version` to provide utility methods.
    """

    def __copy__(self):
        """
        As `__init__()` only accepts a version string as opposed to
        version segments as parameters, we make it easy to copy
        a version object into another one.
        """
        new_version = Version(str(self))
        new_version._version = copy(self._version)
        _reset_sort_key(new_version)
        return new_version

    def next_major(self) -> "Version":
        """
        Return a new `Version` with the next major version.
        """
        version = copy(self)
        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=(version.major + 1, 0, 0),
            pre=version.pre,
            post=version.post,
            dev=version.dev,
            local=version.local,
        )
        _reset_sort_key(version)
        return version

    def next_minor(self) -> "Version":
        """
        Return a new `Version` with the next minor version.
        """
        version = copy(self)
        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=(version.major, version.minor + 1, 0),
            pre=version.pre,
            post=version.post,
            dev=version.dev,
            local=version.local,
        )
        _reset_sort_key(version)
        return version

    def next_micro(self) -> "Version":
        """
        Return a new `Version` with the next micro version.
        """
        version = copy(self)
        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=(version.major, version.minor, version.micro + 1),
            pre=version.pre,
            post=version.post,
            dev=version.dev,
            local=version.local,
        )
        _reset_sort_key(version)
        return version

    def next_alpha(self, with_minor_bump=True, with_major_bump=False) -> "Version":
        """
        Return a new `Version` with the next alpha version.
        Alpha is a segment in a prerelease defined in PEP440.
        """
        version = copy(self)
        if with_major_bump:
            version = version.next_major()
        elif with_minor_bump:
            version = version.next_minor()

        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=version.release,
            pre=_increment_prerelease(version.pre, ALPHA_SEGMENT),
            post=version.post,
            dev=version.dev,
            local=version.local,
        )
        _reset_sort_key(version)
        return version

    def next_beta(self, with_minor_bump=True, with_major_bump=False) -> "Version":
        """
        Return a new `Version` with the next beta version.
        Beta is a segment in a prerelease defined in PEP440.
        """
        version = copy(self)
        if with_major_bump:
            version = version.next_major()
        elif with_minor_bump:
            version = version.next_minor()

        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=version.release,
            pre=_increment_prerelease(version.pre, BETA_SEGMENT),
            post=version.post,
            dev=version.dev,
            local=version.local,
        )
        _reset_sort_key(version)
        return version

    def next_release_candidate(
        self, with_minor_bump=True, with_major_bump=False
    ) -> "Version":
        """
        Return a new `Version` with the next release candidate version.
        Release candidate is a segment in a prerelease defined in PEP440.
        """
        version = copy(self)
        if with_major_bump:
            version = version.next_major()
        elif with_minor_bump:
            version = version.next_minor()

        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=version.release,
            pre=_increment_prerelease(version.pre, RC_SEGMENT),
            post=version.post,
            dev=version.dev,
            local=version.local,
        )
        _reset_sort_key(version)
        return version


def _increment_prerelease(
    prerelease: Optional[Tuple[Text, int]], segment: Text
) -> Tuple[Text, int]:
    """
    Increment a prerelease tuple.
    """
    if not prerelease:
        return (segment, 1)

    current_segment, number = prerelease
    if current_segment == segment:
        return (current_segment, number + 1)

    return (segment, 1)


def _reset_sort_key(version: Version):
    """
    `packaging.version.Version` relies on a sort key for
    sorting version.
    """
    version._key = _cmpkey(
        version._version.epoch,
        version._version.release,
        version._version.pre,
        version._version.post,
        version._version.dev,
        version._version.local,
    )
