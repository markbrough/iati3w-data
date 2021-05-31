""" Import data from the latest Somalia 3W 

Usage:

    python3 -m iati3w.activities_3w downloads/3w-*.csv > output/3w-data.json

"""

import hxl, hashlib, json, sys

from .common import *

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
    ]).encode("utf-8")).hexdigest()[:8]


def fix_cluster_name (name):
    """ Look up the normalised version of a cluster name """
    table = get_lookup_table("inputs/humanitarian-cluster-map.json")
    key = make_token(name)
    if key in table and "name" in table[key]:
        return table[key]["name"]
    else:
        return normalise_string(name)

def get_entity_key (entity):
    """ At this stage, we want to use the entity stub if it's recognised, but keep the entity name if it's not """
    key = "name" if entity.get("unrecognised", False) else "stub"
    return entity[key]

#
# Read Somalia 3W activities via the HXL Proxy (which adds HXL hashtags)
#

def make_activity(row):
    """ Construct an activity object from the HXL row provided """
    
    # Rough in the activity object (fill in details later)
    data = {
        "identifier": None,
        "source": "3W",
        "reported_by": None,
        "humanitarian": True,
        "title": row.get("#activity+programme", default=row.get("#activity+project")),
        "description": row.get("#activity+project"),
        "active": row.get("#status") == "Ongoing",
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
        "modalities": [],
        "targeted": {},
    }

    # add the clusters
    add_unique(fix_cluster_name(row.get("#sector")), data["sectors"]["humanitarian"])

    # add the locations
    admin1 =  lookup_location(row.get("#adm1+name"))
    admin2 = lookup_location(row.get("#adm2+name"))
    loc = lookup_location(row.get("#loc+name"))

    if (admin2 is None or admin2["level"] != "admin2") and loc is not None:
        if loc["level"] == "admin2":
            # For Banadir, especially, the loc can really be the admin2
            admin2 = loc
            loc = None
        elif loc.get("admin2", None) is not None:
            # Or else the loc can imply the admin2
            admin2 = lookup_location(loc["admin2"])

    if "admin1" in admin2 and admin2["admin1"] != make_token(admin1["name"]):
        # Trust the district over the region for 3W (if they conflict)
        admin1 = lookup_location(admin2["admin1"])

    if admin1 is not None and admin1["level"] == "admin1":
        add_unique(get_entity_key(admin1), data["locations"]["admin1"])

    if admin2 is not None and admin2["level"] == "admin2":
        add_unique(get_entity_key(admin2), data["locations"]["admin2"])

    if loc is not None and loc["level"] == "unclassified":
        add_unique(get_entity_key(admin2), data["locations"]["admin2"])

    # add the participating organisations
    for params in [
            ["#org+impl", "implementing"],
            ["#org+prog", "programming"],
            ["#org+funding", "funding"],
    ]:
        org_name = row.get(params[0])
        if org_name:
            org = lookup_org(org_name, create=True)
            if org is not None and not org.get("skip", False):
                # Add the name here instead of the stub if the org isn't in the map
                # lookup_org() will recreate the record for index-orgs.py, which
                # will switch to the stub
                add_unique(get_entity_key(org), data["orgs"][params[1]])

                # for the Somalia 3W, the programming org is the reporter
                if params[1] == "programming":
                    data["reported_by"] = get_entity_key(org)

    # add modality (e.g. for cash programming)
    modality = normalise_string(row.get("#modality"))
    if modality and not is_empty(modality):
        data["modalities"].append(modality)

    # add intended targeted
    for params in [
            ["#targeted+ind+all", "total_individuals"],
            ["#targeted+hh+all", "total_households"],
            ["#targeted+f+adults", "women"],
            ["#targeted+m+adults", "men"],
            ["#targeted+f+children", "girls"],
            ["#targeted+m+children", "boys"],
    ]:
        try:
            s = normalise_string(row.get(params[0]))
            if not is_empty(s):
                v = int(s)
                data["targeted"][params[1]] = v
        except:
            pass


    # Generate pseudo-identifier
    data["identifier"] = make_pseudo_identifier(data)

    return data

    

def fetch_3w(filenames):
    """ Fetch 3W data from all the filenames provided """

    result = []
    for filename in filenames:
        for row in hxl.data(filename, allow_local=True):
            data = make_activity(row)
            result.append(data)
    return result


#
# Script entry point
#

if __name__ == "__main__":
    data = fetch_3w(sys.argv[1:])
    print("Found {} 3W activities".format(len(data)), file=sys.stderr)
    json.dump(data, sys.stdout, indent=4)

# end
