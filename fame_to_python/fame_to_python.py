##################################
# Author: Magnus Kvåle Helliesen #
# mkh@ssb.no                     #
##################################


from os import system
import subprocess as sp

def fame_to_python(
    databases,
    frequency,
    date_span,
    search): #-> pd.DataFrame:
    """
    Converts data from Fame databases to a string representation.

    Parameters:
    - databases (list): List of Fame databases to access (with full path).
    - frequency (str): Frequency of the data ('a', 'q', 'm)'.
    - date_span (tuple): Start and end dates for the data (in Fame syntax, eg. 2023:1 or 2023, depending on frequency).
    - search (str): Query string for fetching specific data.

    Returns:
    str: String representation of Fame data fetched based on the provided parameters.
    """

    # Check that Fame is installed on server
    if system('echo | fame >//dev//null') != 0:
        raise RuntimeError('Fame is not found')

    # If not error is raised, make empty list with Fame commands
    fame_commands = []

    # Add load of flatfile procedure
    fame_commands += 'load \\"fame_to_python/flatfil\\"',

    # Add open databases
    for i, database in enumerate(databases):
        fame_commands += f'open <access read> \\"{database}\\" as db{i}',

    # Add set frequency
    fame_commands += f'frequency {frequency}',

    # Add set date span
    fame_commands += f'date {date_span[0]} to {date_span[1]}',

    # Add call flatfile
    fame_commands += f'\$flatfil \\"{search}\\"',

    # Send Send Fame commands to Fame and store output as string
    full_output = sp.getoutput(f'echo "{";".join(fame_commands)}" | fame')

    # Return output, cropped such that only data are included
    return '\n'.join((full_output.split('\n'))[8:-7])
