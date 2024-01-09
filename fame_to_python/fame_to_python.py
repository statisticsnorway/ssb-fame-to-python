##################################
# Author: Magnus Kvåle Helliesen #
# mkh@ssb.no                     #
##################################


#import pandas as pd
from os import system

def fame_to_python(
    databases,
    frequency,
    date_span,
    search): #-> pd.DataFrame:

    # Check that Fame is installed on server
    if system('echo | fame') != 0:
        raise RuntimeError('Fame is not found')

    # Build list with Fame commands
    commands = []

    # Add load of flatfile procedure
    commands += 'load \\"fame_to_python/flatfile\\"',

    # Add open databases
    for i, database in enumerate(databases):
        commands += f'open <access read> \\"{database}\\" as db{i}',

    # Add set frequency
    commands += f'frequency {frequency}',

    # Add set date span
    commands += f'date {date_span[0]} to {date_span[1]}',

    # Add call flatfile
    commands += f'\$flatfil \\"{search}\\"',

    # Send Send Fame commands to Fame
    system(f'echo "{";".join(commands)}" | fame')
