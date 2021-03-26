""" Import data from the latest Somalia 3W """

import hxl, hashlib, json

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
            "dac": [],
            "humanitarian": [],
        },
        "locations": {
            "countries": ["SO"],
            "admin1": [],
            "admin2": [],
            "unclassified": [],
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
    add_item(data["sectors"]["humanitarian"], row.get("#sector"))

    # add the locations
    add_item(data["locations"]["admin1"], row.get("#adm1+name"))
    add_item(data["locations"]["admin2"], row.get("#adm2+name"))
    add_item(data["locations"]["unclassified"], row.get("#loc+name"))

    # Generate pseudo-identifier
    data["identifier"] = make_pseudo_identifier(data)

    result.append(data)
    
print(json.dumps(result, indent=4))

# end

