# SSB Fame To Python

[![PyPI](https://img.shields.io/pypi/v/ssb-fame-to-python.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/ssb-fame-to-python.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/ssb-fame-to-python)][pypi status]
[![License](https://img.shields.io/pypi/l/ssb-fame-to-python)][license]

[![Documentation](https://github.com/statisticsnorway/ssb-fame-to-python/actions/workflows/docs.yml/badge.svg)][documentation]
[![Tests](https://github.com/statisticsnorway/ssb-fame-to-python/actions/workflows/tests.yml/badge.svg)][tests]
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_ssb-fame-to-python&metric=coverage)][sonarcov]
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_ssb-fame-to-python&metric=alert_status)][sonarquality]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)][poetry]

[pypi status]: https://pypi.org/project/ssb-fame-to-python/
[documentation]: https://statisticsnorway.github.io/ssb-fame-to-python
[tests]: https://github.com/statisticsnorway/ssb-fame-to-python/actions?workflow=Tests

[sonarcov]: https://sonarcloud.io/summary/overall?id=statisticsnorway_ssb-fame-to-python
[sonarquality]: https://sonarcloud.io/summary/overall?id=statisticsnorway_ssb-fame-to-python
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[poetry]: https://python-poetry.org/

## Features

The package is imported using

```python
from fython import fame_to_pandas, fame_to_csv
```

To load data from Fame-databases into a [Pandas](https://pandas.pydata.org/) DataFrame, use

```python
df = fame_to_pandas(['path/to/database1', 'path/to/database2', ...], 'q', '2023:1', '2024:4', 'your_search_query')
```

To load write data from Fame-databases to a csv-file, use

```python
fame_to_csv(['path/to/database1', 'path/to/database2', ...], 'q', '2023:1', '2024:4', 'your_search_query', 'path/to/csv-file')
```

The search query should containg text and/or the wildcards "?" and/or "^" (*any number* of characters and *exactly one* character, respectively).
Both functions have an optional ```decimals``` option (default is 10). ```fame_to_pandas``` has the option ```dtype``` (default is ```np.float128```).

## Requirements
- python-versions = ">=3.6,<4.0"
- pandas = ">=1.1.5"

## Installation

```console
pip install ssb-fame-to-python
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_SSB Fame To Python_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [Statistics Norway]'s [SSB PyPI Template].

[statistics norway]: https://www.ssb.no/en
[pypi]: https://pypi.org/
[ssb pypi template]: https://github.com/statisticsnorway/ssb-pypitemplate
[file an issue]: https://github.com/statisticsnorway/ssb-fame-to-python/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/statisticsnorway/ssb-fame-to-python/blob/main/LICENSE
[contributor guide]: https://github.com/statisticsnorway/ssb-fame-to-python/blob/main/CONTRIBUTING.md
[reference guide]: https://statisticsnorway.github.io/ssb-fame-to-python/reference.html
