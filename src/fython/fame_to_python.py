##################################
# Author: Magnus Kvåle Helliesen #
# mkh@ssb.no                     #
##################################


import subprocess as sp
from io import StringIO
from os import system
from pathlib import Path

import numpy as np
import pandas as pd


def _from_fame(
    databases: list[str],
    frequency: str,
    date_from: str,
    date_to: str,
    search_string: str,
    decimals: int = 10,
) -> str:
    """Fetches data from Fame databases and returns it as a string.

    Parameters
    ----------
    databases : list
        List of Fame databases to access (with full path).
    frequency : str
        Frequency of the data ('a', 'q', 'm').
    date_from : str
        Start date for the data in Fame syntax (e.g., '2023:1' for quarterly, '2023' for annual).
    date_to : str
        End date for the data in Fame syntax (e.g., '2024:4' for quarterly, '2024' for annual).
    search_string : str
        Query string for fetching specific data.
        The search is not case sensitive, and "^" and "?" are wildcards
        (for exactly one and any number of characters, respectively)
    decimals : int, optional
        Number of decimal places in the fetched data (default is 10).

    Returns:
    -------
    str
        String representation of Fame data fetched based on the provided parameters.
    """
    # Store path to this file
    package_path = Path(__file__).resolve().parent

    # Check that Fame is installed on server
    if not _has_fame():
        raise RuntimeError("Fame is not found")

    print("Fetching data, please wait")

    # If no error is raised, make empty list with Fame commands
    fame_commands: list[str] = []

    # Add load of flatfile procedure
    fame_commands += (f'load \\"{package_path / "flatfil"}\\"',)

    # Add decimals option
    fame_commands += (f"decimals {decimals}",)

    # Add open databases
    for i, database in enumerate(databases):
        fame_commands += (f'open <access read> \\"{database}\\" as db{i}',)

    # Add set frequency
    fame_commands += (f"frequency {frequency}",)

    # Add set date span
    fame_commands += (f"date {date_from} to {date_to}",)

    # Add call flatfile-procedure
    fame_commands += (f'\$flatfil \\"{search_string}\\"',)

    return _run_fame_commands(fame_commands)


def _has_fame() -> bool:
    """Returns true if Fame is detected, and false otherwise."""
    return system("echo | fame >//dev//null") == 0


def _run_fame_commands(fame_commands: list[str]) -> str:
    """Execute a list of Fame commands.

    Args:
        fame_commands: A list of Fame commands to be executed.

    Returns:
        The output/result of the executed Fame commands as a string.
    """
    # Send commands to Fame and store output as list of strings
    fame_output = (sp.getoutput(f'echo "{";".join(fame_commands)}" | fame')).split("\n")

    # Find beginning and end of relevant output (Fame return "*" before and after)
    subset = [i for i, x in enumerate(fame_output) if "*" in x]

    # Return subset of output as string
    return "\n".join(fame_output[subset[0] + 1 : subset[1] - 4])


def fame_to_pandas(
    databases: list[str],
    frequency: str,
    date_from: str,
    date_to: str,
    search_string: str,
    decimals: int = 10,
    dtype: type = np.float64,
) -> pd.DataFrame:
    """Converts data from Fame databases to a Pandas DataFrame with PeriodIndex.

    Parameters
    ----------
    databases : list
        List of Fame databases to access (with full path).
    frequency : str
        Frequency of the data ('a', 'q', 'm').
    date_from : str
        Start date for the data in Fame syntax (e.g., '2023:1' for quarterly, '2023' for annual).
    date_to : str
        End date for the data in Fame syntax (e.g., '2024:4' for quarterly, '2024' for annual).
    search_string : str
        Query string for fetching specific data.
        The search is not case sensitive, and "^" and "?" are wildcards
        (for exactly one and any number of characters, respectively)
    decimals : int, optional
        Number of decimal places in the fetched data (default is 10).
    dtype : type, optional
        Type of TBD.

    Returns:
    -------
    pandas.DataFrame
        DataFrame containing Fame data fetched based on the provided parameters.
        The index is a PeriodIndex with the specified frequency.

    Example:
    -------
    >>> df = fame_to_pandas(['path/to/database1', 'path/to/database2'], 'q', '2023:1', '2024:4', 'your_search_query')
    """
    # Get data from Fame
    fame_data = _from_fame(
        databases, frequency, date_from, date_to, search_string, decimals
    )

    # Store data as DataFrame
    output_df = pd.read_csv(StringIO(fame_data), sep=";", index_col=0)
    output_df.index = pd.PeriodIndex(output_df.index, freq=frequency)
    output_df = output_df.astype(dtype)

    print("Done")

    # Return DataFrame
    return output_df


def fame_to_csv(
    databases: list[str],
    frequency: str,
    date_from: str,
    date_to: str,
    search_string: str,
    path: str,
    decimals: int = 10,
) -> None:
    """Fetches data from Fame databases and writes it to a CSV file.

    Parameters
    ----------
    databases : list
        List of Fame databases to access (with full path).
    frequency : str
        Frequency of the data ('a', 'q', 'm').
    date_from : str
        Start date for the data in Fame syntax (e.g., '2023:1' for quarterly, '2023' for annual).
    date_to : str
        End date for the data in Fame syntax (e.g., '2024:4' for quarterly, '2024' for annual).
    search_string : str
        Query string for fetching specific data.
        The search is not case sensitive, and "^" and "?" are wildcards
        (for exactly one and any number of characters, respectively)
    path : str
        Path to the CSV file to be created.
    decimals : int, optional
        Number of decimal places in the fetched data (default is 10).

    Raises:
    ------
    FileNotFoundError
        If the specified path or its directory does not exist.

    Notes:
    -----
    The CSV file is created with the same name as the provided path with a .csv extension.

    Example:
    -------
    >>> fame_to_csv(['database1', 'database2'], 'q', '2023:1', '2024:4', 'search_query', '/path/to/output')
    """
    # Get data from Fame
    fame_data = _from_fame(
        databases, frequency, date_from, date_to, search_string, decimals
    )

    # Make sure extension is .csv and turn into Path object
    path_with_extension = Path(f'{path.split(".")[0]}.csv')

    # Write to csv
    path_with_extension.write_text(fame_data)

    print("Done")
