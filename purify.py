#!/usr/bin/env python

# Not exactly working properly

import os
import sys
import argparse
import re

# The characters that should be replaced by underscores
UNDERSCORE = ['\.', '-', ' ']
UNDERSCORE_PATTERN = '|'.join(UNDERSCORE)

# The characters that should be converted to empty
EMPTY = ['\[.*\]', '\(', '\)', '!', '\?']
EMPTY_PATTERN = '|'.join(EMPTY)

# Files that we want to completely ignore
IGNORE = ['desktop.ini', 'movies.txt']

ASK = 'Accept change? y/n/m (modify): '

# Returns a prettier version of the original name
def prettify(original):
    new_name = re.sub(EMPTY_PATTERN, '', original)
    new_name = new_name.strip()
    new_name = re.sub(UNDERSCORE_PATTERN, '_', new_name)
    new_name = new_name.strip()

    if re.search('dvd', new_name, re.IGNORECASE):
        new_name = re.sub('_?dvd.*', '-D', new_name, flags=re.IGNORECASE)
    else:
        try:
            match = re.search('(.*)_([0-9]{4})', new_name)
            fin = '_'.join(str(k) for k in match.groups())
            fin = fin + '-B'
            new_name = fin
        except:
            print 'Found no match for B'

    return new_name

# Asks the user if they would like to accept the change
def prompt_for_change(curr_abs_path, new_abs_path, path):
    response = raw_input(ASK).lower().strip()
    if response in ['y', 'Yes']:
        os.rename(curr_abs_path, new_abs_path)
        print 'Success!\n'
    elif response in ['m', 'modify'] :
        newname = raw_input('Enter new file name: ').strip()
        os.rename(curr_abs_path, os.path.join(path, newname))
        print 'Succes! Renamed to... {0}\n'.format(newname)
    else:
        print 'Change denied!\n'

def main(argv=None):
    if argv is None:
        argv = sys.argv

    ######################################
    # Parse the arguments
    ######################################
    parser = argparse.ArgumentParser(description='Manipulate file names to a \
                                     human readable format')

    parser.add_argument('PATH', help='location of files to manipulate')
    parser.add_argument('-f', '--file', action='store_true', default=False,
                        help='Interpret PATH as a single file')
    parser.add_argument('-p', '--prompt', action='store_true', default=False,
                        help='Prompt for each file name change')

    args = parser.parse_args()
    path = os.path.expanduser(args.PATH) # Make sure to expand '~'

    # If provided path doesn't exist, then die
    if not os.path.exists(path):
        sys.exit('Path does not exist')

    # Get the list of files in the given directory
    files = os.listdir(path)
    for file in files:
        if file in IGNORE:
            continue

        # Get the absolute path of the file
        curr_abs_path = os.path.join(path, file)

        # Skip the file if it is not a directory
        if not os.path.isdir(curr_abs_path):
            continue

        new_file = prettify(file)
        new_abs_path = os.path.join(path, new_file)

        # If there were no changes then skip it
        if file == new_file:
            continue

        print 'Original Name: ' + file
        print 'New Name: ' + new_file

        if args.prompt:
            prompt_for_change(curr_abs_path, new_abs_path, path)
        else:
            os.rename(curr_abs_path, new_abs_path)

if __name__ == "__main__":
    sys.exit(main())
