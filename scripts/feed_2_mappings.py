#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script for moving characters from the feed to the mappings."""

from xntwist_python_sdk import xntwist_python

# assume there is a configuration file in the current directory
CONFIG_FILE_PATH = "./xn.conf"


def main():
    """."""
    # instantiate an instance of the XN-Twist Python SDK
    xn_sdk = xntwist_python.XnTwistSDK(CONFIG_FILE_PATH)

    # retrieve all of the items from the feed
    items_in_feed = xn_sdk.get_feed()['_items']
    existing_mappings = xn_sdk.get_mappings()['_items']
    mapped_characters = {}

    for mapping in existing_mappings:
        # create a list with only the mapped characters
        mapped_characters[mapping['character']] = mapping['potential_spoofs']

    print(mapped_characters)
    print("\n\n\n")
    # print(existing_mappings)

    # add them to the mappings branch of the API
    for item in items_in_feed:
        # if this character has already been mapped...
        if item['character'] in mapped_characters.keys():
            # see if the spoof character has already been mapped to the character
            new_spoof = True

            for possible_spoof in mapped_characters[item['character']]:
                if item['spoof'] == possible_spoof['spoof_character']:
                    # TODO: make sure this increments properly (1)
                    # update the number of votes for the spoof
                    possible_spoof['votes'] += 1
                    updated_mapping = {
                        'character': item['character'],
                        'potential_spoofs': mapped_characters[item['character']]
                    }
                    new_spoof = False
                    # update the mapping
                    xn_sdk.update_existing_mapping(item, updated_mapping)
                    # TODO: Also need to update the local dataset (1) - I think this will be taken care of, but need to test it out
                    break

            # if this spoof character has never been mapped to this character, add the new, potential spoof
            if new_spoof:
                mapped_characters[item['character']].append({
                    'votes': 1,
                    'spoof_character': item['spoof']
                })
                updated_mapping = {
                    'character': item['character'],
                    'potential_spoofs': mapped_characters[item['character']]
                }
                # update the mapping
                xn_sdk.update_existing_mapping(item, updated_mapping)
        # if this character has not been mapped yet
        else:
            new_mapping = {
                'character': item['character'],
                'potential_spoofs': [{
                    'spoof_character': item['spoof'],
                    'votes': 1
                }]
            }
            # add the new mapping to the API
            xn_sdk.add_new_mapping(new_mapping)
            # add the newly mapped character to the local copy of mapped chars.
            mapped_characters.append(item['character'])


if __name__ == '__main__':
    main()
