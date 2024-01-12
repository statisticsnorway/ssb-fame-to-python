##################################
# Author: Magnus Kvåle Helliesen #
# mkh@ssb.no                     #
##################################


from os import system, path
import subprocess as sp
from io import StringIO
import pandas as pd

def _from_fame(
    databases,
    frequency,
    date_from,
    date_to,
    search_string,
    decimals=10):
    """
    Fetches data from Fame databases and returns it as a string.

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

    Returns
    -------
    str
        String representation of Fame data fetched based on the provided parameters.
    """

    package_path = path.dirname(path.abspath(__file__))

    # Check that Fame is installed on server
    if system('echo | fame >//dev//null') != 0:
        raise RuntimeError('Fame is not found')

    print('Fetching data, please wait')

    # If no error is raised, make empty list with Fame commands
    fame_commands = []

    # Add load of flatfile procedure
    fame_commands += f'load \\"{package_path}/flatfil\\"',

    # Add decimals option
    fame_commands += f'decimals {decimals}',    

    # Add open databases
    for i, database in enumerate(databases):
        fame_commands += f'open <access read> \\"{database}\\" as db{i}',

    # Add set frequency
    fame_commands += f'frequency {frequency}',

    # Add set date span
    fame_commands += f'date {date_from} to {date_to}',

    # Add call flatfile-procedure
    fame_commands += f'\$flatfil \\"{search_string}\\"',

    # Send commands to Fame and store output as list of strings
    fame_output = (sp.getoutput(f'echo "{";".join(fame_commands)}" | fame')).split('\n')

    # Find beginning and end of relevant output (Fame return "*" before and after)
    subset = [i for i, x in enumerate(fame_output) if '*' in x]

    # Return subset of output as string
    return '\n'.join((fame_output)[subset[0]+1:subset[1]-4])


def fame_to_pandas(
    databases,
    frequency,
    date_from,
    date_to,
    search_string,
    decimals=10):
    """
    Converts data from Fame databases to a Pandas DataFrame with PeriodIndex.

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

    Returns
    -------
    pandas.DataFrame
        DataFrame containing Fame data fetched based on the provided parameters.
        The index is a PeriodIndex with the specified frequency.

    Example
    -------
    >>> df = fame_to_pandas(['path/to/database1', 'path/to/database2'], 'q', '2023:1', '2024:4', 'your_search_query')
    """

    # Get data from Fame
    fame_data = _from_fame(
        databases,
        frequency,
        date_from,
        date_to,
        search_string,
        decimals
    )

    # Store data as DataFrame
    output_df = pd.read_csv(StringIO(fame_data), sep=';', index_col=0)
    output_df.index = pd.PeriodIndex(output_df.index, freq=frequency)

    print('Done')

    # Return DataFrame
    return output_df


def fame_to_csv(
    databases,
    frequency,
    date_from,
    date_to,
    search_string,
    path,
    decimals=10):
    """
    Fetches data from Fame databases and writes it to a CSV file.

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

    Raises
    ------
    FileNotFoundError
        If the specified path or its directory does not exist.

    Notes
    -----
    The CSV file is created with the same name as the provided path with a .csv extension.

    Example
    -------
    >>> fame_to_csv(['database1', 'database2'], 'q', '2023:1', '2024:4', 'search_query', '/path/to/output')
    """

    # Get data from Fame
    fame_data = _from_fame(
        databases,
        frequency,
        date_from,
        date_to,
        search_string,
        decimals
    )

    # Make sure extension is .csv
    path_with_extension = f'{path.split(".")[0]}.csv'

    # Write string to file
    with open(path_with_extension, 'w') as file_handle:
        print(f'Writing to {path_with_extension}')
        file_handle.write(fame_data)
        print('Done')
