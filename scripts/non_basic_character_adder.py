#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to add characters to the list of non_basic_characters which are mapped to latin characters."""

import argparse
import os
import string

from xn_twist_python_sdk import xn_twist_python

# assume there is a configuration file in the current directory
CONFIG_FILE_PATH = "./xn.conf"


def parse_arguments():
    """."""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('text', help='text containing the characters to be added')

    args = parser.parse_args()
    return args


def main():
    """Back up the mappings."""
    args = parse_arguments()

    # get all of the mappings
    xn_sdk = xn_twist_python.XnTwistSDK(os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG_FILE_PATH)))

    non_basic_characters = xn_sdk.get_branch('non_basic_characters')['_items']
    # create a list with only the non_basic_characters
    existing_characters = [char['potential_spoof'] for char in non_basic_characters]
    # add the basic numbers and Latin characters to prevent them from being added
    existing_characters.extend(string.printable)

    # iterate through the given text, checking to see if the character is already in the dataset. If not, add it.
    for char in args.text:
        if char not in existing_characters and char != ' ':
            # add the character to the api
            xn_sdk.add_item({
                'potential_spoof': char
            }, 'non_basic_characters')
            # add the character to the list of existing characters
            existing_characters.extend(char)
            print("Added: {}".format(char))


if __name__ == '__main__':
    main()
