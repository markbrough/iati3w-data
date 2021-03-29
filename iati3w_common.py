""" Common variables and functions for all scripts

"""

import re

ROLES = ["implementing", "programming", "funding"]
SECTOR_TYPES = ["dac", "humanitarian"]
LOCATION_TYPES = ["admin1", "admin2", "unclassified"]


def normalise_string (s):
    """ Normalise whitespace in a string.
    Preserve character case and punctuation

    """
    return re.sub(r'\W+', ' ', s.strip())

def tokenise_string (s):
    """ Create a lookup token from a string.
    Normalise space, convert to lowercase, and remove punctuation

    """
    return re.sub(r'[^\w+]', ' ', s.strip().lower())
               

