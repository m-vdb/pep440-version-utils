All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/) and [PEP440](https://peps.python.org/pep-0440/)
starting with version 0.1.

## [1.2.0] - 2025-09-24

### Improvements

- Add support for Python 3.13.

## [1.1.1] - 2024-08-29

### Maintenance

- Bump dependency constraint on `packaging`.

## [1.1.0] - 2024-06-14

### Improvements

- Add support for Python 3.11.
- Add support for Python 3.12.

### Bug fixes

- Fix the behaviour of `Version.next_micro()`, `Version.next_minor()` and `Version.next_major()` when a dev version is already present.

## [1.0.0] - 2023-11-29

### Improvements

- Add support for Python 3.10.
- Bump `packaging` to `^23.2`` while loosening version constraint.

### Removal & Deprecations

- Remove support for Python 3.6 and Python 3.7. Both versions reached end of life.
