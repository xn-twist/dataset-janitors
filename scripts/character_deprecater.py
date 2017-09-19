#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Removed characters suggested for deprecation from the list of possible spoofs."""

import os

from xn_twist_python_sdk import xn_twist_python

# assume there is a configuration file in the current directory
CONFIG_FILE_PATH = "./xn.conf"
CHARACTER_DEPRECATION_THRESHOLD = 10


def main():
    """Move characters from the feed to the mappings."""
    # instantiate an instance of the XN-Twist Python SDK
    xn_sdk = xn_twist_python.XnTwistSDK(os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG_FILE_PATH)))

    # get the characters that have been suggested for deprecation
    suggestions = xn_sdk.get_branch("suggested_deprecations")['_items']
    suggested_deprecation_count = {}

    non_basic_characters = xn_sdk.get_branch("non_basic_characters")['_items']

    for suggestion in suggestions:
        if suggested_deprecation_count.get(suggestion['character']):
            suggested_deprecation_count[suggestion['character']] += 1
        else:
            suggested_deprecation_count[suggestion['character']] = 1

    for key in suggested_deprecation_count:
        # if the character has been voted for deprecation too many times...
        if suggested_deprecation_count[key] > CHARACTER_DEPRECATION_THRESHOLD:
            # add the character to the list of deprecated characters
            xn_sdk.add_item({"deprecated_character": key},
                            "deprecated_characters")

            # delete the character from the list of suggested deprecations
            for suggestion in suggestions:
                # if the character in the suggestion is the one we are deprecating, remove it from the list of suggestions
                if suggestion['character'] == key:
                    xn_sdk.delete(suggestion, "suggested_deprecations")

            # delete the character from the list of non_basic_characters
            for char in non_basic_characters:
                if char['potential_spoof'] == key:
                    xn_sdk.delete(char, "non_basic_characters")
                    break


if __name__ == '__main__':
    main()
