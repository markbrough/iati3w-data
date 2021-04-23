""" Common variables and functions for all scripts

"""

import json, re, string

from hxl.datatypes import is_empty

#
# Keys for classifying things
#
ROLES = ["implementing", "programming", "funding",]
SCOPES = ["local", "regional", "international", "unknown",]
SECTOR_TYPES = ["dac", "humanitarian",]
LOCATION_TYPES = ["admin1", "admin2", "unclassified",]


#
# Utility functions
#

def add_unique (element, l, key=None):
    """ Add an element to a list if it's not already in a list and isn't falsey
    If key is not None, assume the value to add is a dict and use the key for uniqueness.
    """

    if not element:
        # don't add if the item is falsely
        pass
    elif key is None:
        # if there's no key, assume a string or something that can be forced to one
        s = str(element)
        if not is_empty(s) and not s in l:
            l.append(element)
    else:
        s = str(element.get(key, ""))
        if not is_empty(s) and not s in [str(v1.get(key, None)) for v1 in l]:
            l.append(element)

    return l

def normalise_string (s):
    """ Normalise whitespace in a string.
    Preserve character case and punctuation

    """
    if not s:
        return None
    else:
        return re.sub(r'\s+', ' ', s.strip())

def make_token (s):
    """ Create a lookup token from a string.
    Normalise space, convert to lowercase, and remove punctuation
    Use max 64 characters.

    """
    return re.sub(r'\W+', ' ', s).lower().strip()[:64]

#
# Look up and manage JSON datasets
#

datasets_loaded = {}

def get_dataset (path):
    global datasets_loaded
    if not path in datasets_loaded:
        with open(path, "r") as input:
            datasets_loaded[path] = json.load(input)
    return datasets_loaded[path]


#
# Lookup tables (transformed from JSON maps)
#

lookup_tables_loaded = {}

def get_lookup_table (path):
    """ Make a lookup table, including synonyms
    Keys will be tokenized

    """
    global lookup_tables_loaded
    if not path in lookup_tables_loaded:
        result = {}
        map = get_dataset(path)
        for key, info in map.items():
            result[make_token(key)] = info
            if "name" in info:
                result.setdefault(make_token(info["name"]), info)
            if "shortname" in info:
                result.setdefault(make_token(info["shortname"]), info)
            for synonym in info.get("synonyms", []):
                result.setdefault(make_token(synonym), info)
        lookup_tables_loaded[path] = result
    return lookup_tables_loaded[path]


org_lookup_failures = set()
""" Org-lookup failures that we've already reported """

def lookup_org (name, show_failures=False, return_default=True):
    """ Look up an org by name """
    if name is None:
        return None

    name = str(name)
    if is_empty(name):
        return None
    token = make_token(name)
    table = get_lookup_table("inputs/org-map.json")

    if token in table:
        return table[token]
    else:
        if show_failures and token not in org_lookup_failures:
            import sys
            print("New org: {}".format(name), file=sys.stderr)
            org_lookup_failures.add(token)
        if return_default:
            return {
                "name": normalise_string(name),
                "shortname": normalise_string(name),
                "scope": "unknown",
            }
        else:
            return None
    

#
# Special lookup tables for locations (which are hierarchical)
#

location_lookup_table = None

def get_location_lookup_table ():
    """ Load and transform the location table if needed, then return """

    global location_lookup_table

    # if it's already loaded, just return
    if location_lookup_table is not None:
        return location_lookup_table

    def add_entry(info, key, admin1=None, admin2=None):
        """ Construct a single, flat entry for a location, and add it under the name and synonyms """
        entry = {
            "name": info["name"],
            "level": info["level"],
        }
        if admin1 is not None:
            entry["admin1"] = admin1
        if admin2 is not None:
            entry["admin2"] = admin2
        for key in ["synonyms", "pcode", "skip"]:
            if key in info:
                entry[key] = info[key]

        # Add the main name
        location_lookup_table.setdefault(make_token(key), entry)
        location_lookup_table.setdefault(make_token(info["name"]), entry)

        # Add the synonyms
        for synonym in info.get("synonyms", []):
            location_lookup_table.setdefault(make_token(synonym), entry)

        if "iati_id" in info:
            locaation_lookup_table.setdefault(make_token(info["iati_id"]), entry)

    location_lookup_table = {}

    map = get_dataset("inputs/location-map.json")

    # We need to go sort-of breadth-first to make sure that higher levels take priority
    # Never overwrite an existing entry (except at the region level)

    # pass 1: regions
    for name, info in map["admin1"].items():
        add_entry(info, key=name)

    # pass 2: districts
    for region_name, region_info in map["admin1"].items():
        for name, info in region_info.get("admin2", {}).items():
            add_entry(info, key=name, admin1=region_name)

    # pass 3: unclassified locations under districts
    for region_name, region_info in map["admin1"].items():
        for district_name, district_info in region_info.get("admin2", {}).items():
            for name, info in district_info.get("unclassified", {}).items():
                add_entry(info, key=name, admin1=region_name, admin2=district_name)

    # pass 4: unclassified locations under regions
    for region_name, region_info in map["admin1"].items():
        for name, info in region_info.get("unclassified", {}).items():
            add_entry(info, key=name, admin1=region_name)

    # pass 5: unclassified locations at the top level
    for name, info in map["unclassified"].items():
        add_entry(info, key=name)

    return location_lookup_table


def lookup_location (name, loctype="unclassified"):
    """ Look up a location name and see what we can do with it """

    # we don't care about empty names
    if is_empty(name):
        return None

    # return the lookup if it exists, or just a cleaned-up name
    token = make_token(name)
    lookup = get_location_lookup_table()
    if not token in lookup:
        lookup[token] = {
            "level": loctype,
            "name": normalise_string(name),
        }
    return lookup[token]
