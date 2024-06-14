![Continuous Integration](https://github.com/m-vdb/pep440-version-utils/workflows/Continuous%20Integration/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/m-vdb/pep440-version-utils/badge.svg?branch=main)](https://coveralls.io/github/m-vdb/pep440-version-utils?branch=main)

# pep440-version-utils
This package regroups utilities to deal with pep440 versioning. It is based on the
[PyPA's `packaging`](https://github.com/pypa/packaging) project and extends it.

It makes it easier to handle version bumps and strictly follows [PEP440 specification](https://www.python.org/dev/peps/pep-0440/).

![Release cycle](https://github.com/m-vdb/pep440-version-utils/blob/main/docs/release-cycle.png?raw=true)

## Installation

Use `pip` or `poetry` to install this package:

```bash
$ pip install pep440-version-utils

# or alternatively
$ poetry add pep440-version-utils
```

## Usage

Since this package extends the `packaging` library, so it supports version parsing and ordering as described
in [this documentation](https://packaging.pypa.io/en/latest/version/).

To bump to a new release version:

```python
from pep440_version_utils import Version

version = Version("1.10.2")
version.next_micro()  # 1.10.3
version.next_minor()  # 1.11.0
version.next_major()  # 2.0.0
```

To bump to a new prerelease version:

```python
from pep440_version_utils import Version

version = Version("1.10.2")
version.next_alpha()  # 1.10.3a1
version.next_beta()  # 1.10.3b1
version.next_release_candidate()  # 1.10.3rc1

version.next_alpha("minor")  # 1.11.0a1
version.next_beta("mior")  # 1.11.0b1
version.next_release_candidate("major")  # 2.0.0rc1
```

And it implements the full release cycle:

```python
from pep440_version_utils import Version

version = Version("1.10.2")
alpha1 = version.next_alpha()  # 1.10.3a1
alpha2 = alpha1.next_alpha()  # 1.10.3a2
beta1 = alpha2.next_beta()  # 1.10.3b1
rc1 = beta1.next_release_candidate()  # 1.10.3rc1
rc2 = rc1.next_release_candidate()  # 1.10.3rc2
new_version = rc2.next_micro()  # 1.10.3
```

You can also check if a version is a specific type of prerelease:
```python
from pep440_version_utils import Version

Version("1.10.2a1").is_alpha  # True
Version("1.10.2b2").is_beta  # True
Version("1.10.2rc1").is_release_candidate  # True
```

## Limitations

This package doesn't support _post_ and _local_ versions yet. **Contributions are welcome 😊**

## How to contribute

This package is fairly simple, here is how you can contribute:

1. ⚙️ Install [`poetry`](https://python-poetry.org/)
2. 📦 In the repository folder, run `poetry install`
3. ✍️ Implement the desired changes
4. ✅ Run test, type checking and code quality checks:
```bash
$ poetry run black . --check
$ poetry run mypy */**.py --ignore-missing-imports
$ poetry run pytest --cov=pep440_version_utils
```
5. ➡️ Submit a new pull request

Do not hesitate to contribue, even for very small changes!

## How to release new versions

1. Update CHANGELOG
2. Update project version in `pyproject.toml`
3. `poetry build`
4. `poetry publish`
