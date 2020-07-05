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
DEV_SEGMENT = "dev"

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
        if not version.is_release and not (version.minor or version.micro):
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
        if not version.is_release and not version.micro:
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
        if not version.is_release and version.micro > 0:
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

    def next_dev(self, version_bump=VERSION_MICRO) -> "Version":
        """
        Return a new `Version` with the next developmental version.
        Dev is a segment in a release, prerelease of postrelease
        defined in PEP440.
        """
        return _next_devrelease_version(self, version_bump)

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

    @property
    def is_release(self) -> bool:
        """
        Return True if the `Version` is a final release.
        """
        return self.public == self.base_version


def _build_suffixed_version(
    version: Version,
    prerelease: Optional[Tuple[Text, int]],
    devrelease: Optional[Tuple[Text, int]],
) -> Version:
    """
    Return a new `Version` including the provided prerelease and optional devrelease.
    """
    version = copy(version)

    version._version = VersionNamedTuple(
        epoch=version._version.epoch,
        release=version.release,
        pre=prerelease,
        post=None,
        dev=devrelease,
        local=None,
    )
    _reset_sort_key(version)
    return version


def _next_devrelease_version(version: Version, version_bump: Text) -> Version:
    """
    Return a new `Version` with the next developmental release (.dev)
    Dev releases can be within final, pre- or post-release release phases.
    It can bump either the major, minor or micro part of the release if there
    the current version has no pre-release, post-release or developmental markers.
    """
    version = copy(version)

    if version.is_release:
        version = _next_release_version(version, version_bump)

    prerelease = None
    if version.pre is not None:
        if version.is_devrelease:
            prerelease = version.pre
        else:
            prerelease_phase = version.pre[0]  # increment the current pre-release phase
            prerelease = _increment_prerelease(version.pre, prerelease_phase)
    devrelease_id = version.dev  # NOTE: Incorrect type annotation in BaseVersion
    devrelease = _increment_devrelease(devrelease_id)  # type: ignore

    return _build_suffixed_version(version, prerelease, devrelease)


def _next_prerelease_version(
    version: Version, version_bump: Text, segment: Text
) -> Version:
    """
    Return a new `Version` with the next prerelease (one of alpha, beta, rc).
    It can bump either the major, minor or micro part of the release, if
    neither a developmental release or a prerelease is being incremented (the
    current version has no dev or prerelease markers).
    """
    version = copy(version)

    if version.is_release:
        version = _next_release_version(version, version_bump)

    prerelease = _increment_prerelease(version.pre, segment)
    devrelease = None
    return _build_suffixed_version(version, prerelease, devrelease)


def _next_release_version(version: Version, version_bump: Text) -> Version:
    """
    Return a new `Version` with the release segment incremented if valid.
    The major, minor or micro part of the release segment will be incremented as
    specified by `version_bump`, and only if the current version is a final release (not
    a developmental, pre or post release).
    """
    if version_bump == VERSION_MAJOR:
        version = version.next_major()
    elif version_bump == VERSION_MINOR:
        version = version.next_minor()
    elif version_bump == VERSION_MICRO:
        version = version.next_micro()
    else:
        # would use typing.Literal but only available in Python 3.8
        raise TypeError(f"Unknown version bump: {version_bump}")
    return version


def _increment_devrelease(devrelease_id: Optional[int]) -> Tuple[Text, int]:
    """
    Increment a developmental release.
    """
    current_tuple = None
    if devrelease_id:
        current_tuple = (DEV_SEGMENT, devrelease_id)
    return _increment_subrelease(current_tuple, DEV_SEGMENT)


def _increment_prerelease(
    prerelease: Optional[Tuple[Text, int]], segment: Text
) -> Tuple[Text, int]:
    """
    Increment a prerelease tuple.
    """
    return _increment_subrelease(prerelease, segment)


def _increment_subrelease(
    type_number_pair: Optional[Tuple[Text, int]], segment: Text
) -> Tuple[Text, int]:
    """
    Increment a part of release (pre, dev or post segment).

    The tuple is a pair of the phase/type and the release number.
    This is a generalised form of the `BaseVersion.pre` value.
    """
    if not type_number_pair:
        return (segment, 1)

    current_segment, number = type_number_pair
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
