""" Import data from the latest Somalia 3W """

import hxl, hashlib, json

from iati3w_common import *

from hxl.datatypes import is_empty

#
# Utility functions
#

def make_pseudo_identifier (data):
    """ Since 3W data doesn't have unique activity identifiers, construct a pseudo one """
    return hashlib.sha256(json.dumps([
        data["title"],
        data["description"],
        data["orgs"],
        data["sectors"],
        data["locations"],
    ]).encode("utf-8")).hexdigest()


def add_item (items, item, condition=None):
    """ Add an item to a list if it's not empty (or optionally, if the condition is true) """
    if (condition is None and not is_empty(item)) or condition:
        items.append(item.strip())

def fix_cluster_name (name):
    """ Look up the normalised version of a cluster name """
    table = get_lookup_table("inputs/humanitarian-cluster-map.json")
    key = make_token(name)
    if key in table and "name" in table[key]:
        return table[key]["name"]
    else:
        return normalise_string(name)

    
#
# Read Somalia 3W activities via the HXL Proxy (which adds HXL hashtags)
#

DATASET = "https://proxy.hxlstandard.org/data/8acb4c"

result = []

for row in hxl.data(DATASET):
    data = {
        "identifier": None,
        "source": "3W",
        "reported_by": "OCHA Somalia",
        "has_humanitarian_content": True,
        "title": row.get("#activity+programme", default=row.get("#activity+project")),
        "description": row.get("#activity+project"),
        "is_active": row.get("#status") == "Ongoing",
        "orgs": {
            "implementing": [],
            "programming": [],
            "funding": [],
        },
        "sectors": {
            "humanitarian": [],
            "dac": [],
        },
        "locations": {
            "unclassified": [],
            "admin2": [],
            "admin1": [],
            "countries": ["SO"],
        },
        "dates": {
            "start": row.get("#date+start"),
            "end": row.get("#date+end"),
        },
    }

    # add the participating organisations
    add_item(data["orgs"]["implementing"], row.get("#org+impl"))
    add_item(data["orgs"]["programming"], row.get("#org+prog")),
    add_item(data["orgs"]["funding"], row.get("#org+funding")),

    # add the clusters
    add_item(data["sectors"]["humanitarian"], fix_cluster_name(row.get("#sector")))

    # add the locations
    add_item(data["locations"]["admin1"], fix_location(row.get("#adm1+name")))
    add_item(data["locations"]["admin2"], fix_location(row.get("#adm2+name")))
    add_item(data["locations"]["unclassified"], fix_location(row.get("#loc+name")))

    # Generate pseudo-identifier
    data["identifier"] = make_pseudo_identifier(data)

    result.append(data)
    
print(json.dumps(result, indent=4))

# end

