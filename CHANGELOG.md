# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- updates to workflow to get automatic version updating to work
  - `src/medutils/__init__.py` was being updated, but not committed.

## [0.4.2] - 2024-12-19
### Fixed
- updates to workflow to get automatic version updating to work]
  - didn't quite fix it

## [0.4.1] - 2024-12-19
### Added
- `--version` option to `merge` command

## [0.4.0] - 2024-12-18
### Added
- `--keep uniq` option for `merge` command
  - keeps only unique values, duplicates are ignored.

## [0.3.1] - 2024-04-24
### Added
- `--ignore` flag for `merge` command
  - specifies columns that will be ignored and not included in the output

## [0.3.0] - 2024-04-22
### Added
- `merge`
  - my version of join(1) that doesn't require sorting

## [0.2.1] - 2024-04-20
### Fixed
- added missing 'getcol' entry to pyproject.toml to get getcol script file created

## [0.2.0] - 2024-04-20
### Added
- `getcol`
  - script to extract columns from a delimited file

## [0.1.1] - 2024-01-19
### Changed
- updated to use cruft and the template https://github.com/collijk/python-package-cookiecutter

## [0.1.0] - 2024-01-19
### Added
- `touch_latest`
  - script to touch (and create if necessary) a file
    with its modification date set to the latest date found in the specified dicrectories

[Unreleased]: https://github.com/malcolm-3/medutils/compare/0.4.2...master
[0.4.2]: https://github.com/malcolm-3/medutils/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/malcolm-3/medutils/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/malcolm-3/medutils/compare/0.3.1...0.4.0
[0.3.1]: https://github.com/malcolm-3/medutils/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/malcolm-3/medutils/compare/0.2.1...0.3.0
[0.2.1]: https://github.com/malcolm-3/medutils/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/malcolm-3/medutils/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/malcolm-3/medutils/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/malcolm-3/medutils/tree/0.1.0
