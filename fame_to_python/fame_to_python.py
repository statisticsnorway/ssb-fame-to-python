##################################
# Author: Magnus Kvåle Helliesen #
# mkh@ssb.no                     #
##################################


from os import system, path
import subprocess as sp
from io import StringIO
import pandas as pd

def fame_to_python(
    databases,
    frequency,
    date_from,
    date_to,
    search_string):
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

    Returns
    -------
    pandas.DataFrame
        DataFrame containing Fame data fetched based on the provided parameters.
        The index is a PeriodIndex with the specified frequency.
    """

    package_path = path.dirname(path.abspath(__file__))

    # Check that Fame is installed on server
    if system('echo | fame >//dev//null') != 0:
        raise RuntimeError('Fame is not found')

    # If not error is raised, make empty list with Fame commands
    fame_commands = []

    # Add load of flatfile procedure
    fame_commands += f'load \\"{package_path}/flatfil\\"',

    # Add open databases
    for i, database in enumerate(databases):
        fame_commands += f'open <access read> \\"{database}\\" as db{i}',

    # Add set frequency
    fame_commands += f'frequency {frequency}',

    # Add set date span
    fame_commands += f'date {date_from} to {date_to}',

    # Add call flatfile
    fame_commands += f'\$flatfil \\"{search_string}\\"',

    # Send Send Fame commands to Fame and store output as string
    full_output = sp.getoutput(f'echo "{";".join(fame_commands)}" | fame')

    # Store data as DataFrame
    output_df = pd.read_csv(StringIO('\n'.join((full_output.split('\n'))[8:-7])), sep=';', index_col=0)
    output_df.index = pd.PeriodIndex(output_df.index, freq=frequency)

    # Return DataFrame
    return output_df
