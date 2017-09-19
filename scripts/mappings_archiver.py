#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to backup the mappings just in case anything goes wrong."""

import json
import os

from xn_twist_python_sdk import xn_twist_python

# assume there is a configuration file in the current directory
CONFIG_FILE_PATH = "./xn.conf"


def main():
    """Back up the mappings."""
    # get all of the mappings
    xn_sdk = xn_twist_python.XnTwistSDK(os.path.abspath(os.path.join(os.path.dirname(__file__), CONFIG_FILE_PATH)))

    mappings = xn_sdk.retrieve_dataset()

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backup/mappings.json")), "w+") as f:
        f.write(json.dumps(mappings))


if __name__ == '__main__':
    main()
