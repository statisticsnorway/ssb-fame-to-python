# ssb-fame-to-python (fython)

Python function to write Fame data to pandas DataFrame

Opprettet av:
Magnus Helliesen <mkh@ssb.no>

---

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
Both functions have an optional ```decimals``` option (default is 10).

## Requirements
- python-versions = ">=3.6,<4.0"
- pandas = ">=1.1.5"

## Installation
```
poetry add git+https://github.com/statisticsnorway/ssb-fame-to-python.git
```

or

```
pip install https://github.com/statisticsnorway/ssb-fame-to-python.git
```
