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

VERSION_MICRO = "micro"
VERSION_MINOR = "minor"
VERSION_MAJOR = "major"


class Version(BaseVersion):
    """
    Supercede `packaging.version.Version` to provide utility methods.
    """

    def __copy__(self) -> "Version":
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
        major = version.major + 1
        if (version.pre or version.dev) and not version.minor and not version.micro:
            major = version.major
        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=(major, 0, 0),
            pre=None,
            post=None,
            dev=None,
            local=None,
        )
        _reset_sort_key(version)
        return version

    def next_minor(self) -> "Version":
        """
        Return a new `Version` with the next minor version.
        """
        version = copy(self)
        minor = version.minor + 1
        if (version.pre or version.dev) and not version.micro:
            minor = version.minor
        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=(version.major, minor, 0),
            pre=None,
            post=None,
            dev=None,
            local=None,
        )
        _reset_sort_key(version)
        return version

    def next_micro(self) -> "Version":
        """
        Return a new `Version` with the next micro version.
        """
        version = copy(self)
        micro = version.micro + 1
        if (version.pre or version.dev) and version.micro > 0:
            micro = version.micro
        version._version = VersionNamedTuple(
            epoch=version._version.epoch,
            release=(version.major, version.minor, micro),
            pre=None,
            post=None,
            dev=None,
            local=None,
        )
        _reset_sort_key(version)
        return version

    def next_alpha(self, version_bump=VERSION_MICRO) -> "Version":
        """
        Return a new `Version` with the next alpha version.
        Alpha is a segment in a prerelease defined in PEP440.
        """
        return _next_prerelease_version(self, version_bump, ALPHA_SEGMENT)

    def next_beta(self, version_bump=VERSION_MICRO) -> "Version":
        """
        Return a new `Version` with the next beta version.
        Beta is a segment in a prerelease defined in PEP440.
        """
        return _next_prerelease_version(self, version_bump, BETA_SEGMENT)

    def next_release_candidate(self, version_bump=VERSION_MICRO) -> "Version":
        """
        Return a new `Version` with the next release candidate version.
        Release candidate is a segment in a prerelease defined in PEP440.
        """
        return _next_prerelease_version(self, version_bump, RC_SEGMENT)

    @property
    def is_alpha(self) -> bool:
        """
        Return True if the `Version` is an alpha.
        """
        return self.pre is not None and self.pre[0] == ALPHA_SEGMENT

    @property
    def is_beta(self) -> bool:
        """
        Return True if the `Version` is a beta.
        """
        return self.pre is not None and self.pre[0] == BETA_SEGMENT

    @property
    def is_release_candidate(self) -> bool:
        """
        Return True if the `Version` is a release candidate.
        """
        return self.pre is not None and self.pre[0] == RC_SEGMENT


def _next_prerelease_version(
    version: Version, version_bump: Text, segment: Text
) -> Version:
    """
    Return a new `Version` with the next prerelease (one of alpha, beta, rc).
    It can bump either the major, minor or micro part of the release, if this
    is the first prerelease (prerelease is absent from the current version).
    """
    version = copy(version)
    if not version.pre:
        if version_bump == VERSION_MAJOR:
            version = version.next_major()
        elif version_bump == VERSION_MINOR:
            version = version.next_minor()
        elif version_bump == VERSION_MICRO:
            version = version.next_micro()
        else:
            # would use typing.Literal but only available in Python 3.8
            raise TypeError(f"Unknown version bump: {version_bump}")

    version._version = VersionNamedTuple(
        epoch=version._version.epoch,
        release=version.release,
        pre=_increment_prerelease(version.pre, segment),
        post=None,
        dev=None,
        local=None,
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
