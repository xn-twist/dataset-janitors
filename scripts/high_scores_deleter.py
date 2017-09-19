#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to delete the high scores every day."""

import os

from xn_twist_python_sdk import xn_twist_python

# assume there is a configuration file in the current directory
CONFIG_FILE_PATH = "./xn.conf"
HIGH_SCORES_PATH = "high_scores"


def main():
    """Move characters from the feed to the mappings."""
    # instantiate an instance of the XN-Twist Python SDK
    xn_sdk = xn_twist_python.XnTwistSDK(os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG_FILE_PATH)))

    # retrieve all of the high scores
    high_scores = xn_sdk.get_branch(HIGH_SCORES_PATH)['_items']

    # delete each of the high scores
    for high_score in high_scores:
        xn_sdk.delete_item(high_score, HIGH_SCORES_PATH)

    # add a placeholder entry
    xn_sdk.add_item({
        'initials': "AAA",
        'score': 5
    }, HIGH_SCORES_PATH)


if __name__ == '__main__':
    main()
