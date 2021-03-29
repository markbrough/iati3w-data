""" Common variables and functions for all scripts

"""

import json, re, string

from hxl.datatypes import is_empty

ROLES = ["implementing", "programming", "funding"]
SECTOR_TYPES = ["dac", "humanitarian"]
LOCATION_TYPES = ["admin1", "admin2", "unclassified"]


def normalise_string (s):
    """ Normalise whitespace in a string.
    Preserve character case and punctuation

    """
    return re.sub(r'\W+', ' ', s.strip())

def make_token (s):
    """ Create a lookup token from a string.
    Normalise space, convert to lowercase, and remove punctuation

    """
    return re.sub(r'[^\w+]', ' ', s.strip().lower())

def fix_location (s):
    if s:
        return string.capwords(normalise_string(s))
    else:
        return ""


location_lookup_table = None

def get_location_lookup_table ():
    """ Load and transform the location table if needed, then return """
    global location_lookup_table

    if location_lookup_table is None:
        location_lookup_table = {}

        with open("inputs/location-map.json", "r") as input:
            map = json.load(input)

        for name1, info1 in map.items():

            # add the region
            token1 = make_token(name1)
            location_lookup_table[token1] = info1

            # add the districts
            for name2, info2 in info1.get("admin2", {}).items():
                token2 = make_token(name2)
                location_lookup_table.setdefault(token2, info2) # only if doesn't exist

                # add the synonyms for the districts
                for name3 in info2.get("synonyms", []):
                    location_lookup_table.setdefault(make_token(name3), info2) # only if doesn't exist

            # add the synonyms for the regions
            for name2 in info1.get("synonyms", []):
                location_lookup_table.setdefault(make_token(name2), info1) # only if doesn't exist

    return location_lookup_table


def lookup_location (name, loctype="unclassified"):
    """ Look up a location name and see what we can do with it """

    # we don't care about empty names
    if is_empty(name):
        return None

    # return the lookup if it exists, or just a cleaned-up name
    return get_location_lookup_table().get(make_token(name), {
        "level": loctype,
        "name": normalise_string(name),
    });

