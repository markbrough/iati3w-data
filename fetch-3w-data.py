""" Import data from the latest Somalia 3W """

import hxl, hashlib, json

from hxl.datatypes import is_empty

#
# Utility functions
#

def make_pseudo_identifier (data):
    """ Since 3W data doesn't have unique activity identifiers, construct a pseudo one """
    return hashlib.sha256("|||".join([
        data["title"],
        data["description"],
        "||".join([org[0] for org in data["orgs"]]),
        "||".join(data["clusters"]),
        "||".join(data["locations"]),
    ]).encode("utf-8")).hexdigest()


def add_item (items, item, condition=None):
    """ Add an item to a list if it's not empty (or optionally, if the condition is true) """
    if (condition is None and not is_empty(item)) or condition:
        items.append(item)
    
    
#
# Read Somalia 3W activities via the HXL Proxy (which adds HXL hashtags)
#

DATASET = "https://proxy.hxlstandard.org/data/8acb4c"

print("[")

for i, row in enumerate(hxl.data(DATASET)):
    data = {
        "identifier": None,
        "source": "Somalia 3W",
        "reported_by": "OCHA Somalia",
        "has_humanitarian_content": True,
        "title": row.get("#activity+programme", default=row.get("#activity+project")),
        "description": row.get("#activity+project"),
        "orgs": {
            "implementing": [],
            "programming": [],
            "funding": [],
        },
        "dac_sectors": [],
        "humanitarian_clusters": [],
        "start_date": row.get("#date+start"),
        "end_date": row.get("#date+end"),
        "is_active": row.get("#status") == "Ongoing",
        "countries": ["SO"],
        "locations": [],
    }

    # add the participating organisations
    add_item(data["orgs"]["implementing"], [row.get("#org+impl"), "implementing"], row.get("#org+impl") is not None)
    add_item(data["orgs"]["programming"], [row.get("#org+prog"), "programming"], row.get("#org+prog") is not None)
    add_item(data["orgs"]["funding"], [row.get("#org+funding"), "funding"], row.get("#org+funding") is not None)
    add_item(data["clusters"], row.get("#sector"))
    for hashtag in ["#adm1+name", "#adm2+name", "#loc+name"]:
        add_item(data["locations"], row.get(hashtag))
    
    # Generate pseudo-identifier
    data["identifier"] = make_pseudo_identifier(data)

    if i > 0:
        print(",")
    print(json.dumps(data, indent=4), end="")

print("]")
    
