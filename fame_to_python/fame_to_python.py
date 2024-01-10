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
    TBA
    """

    # Check that Fame is installed on server
    if system('echo | fame >\\dev\\null') != 0:
        raise RuntimeError('Fame is not found')

    # Build list with Fame commands
    fame_commands = []

    # Add load of flatfile procedure
    fame_commands += 'load \\"fame_to_python/flatfile\\"',

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
