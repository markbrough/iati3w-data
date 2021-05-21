""" Create a JSON index with information about each sector in the activities

Usage:

    python3 -m iati3w.sector_index output/3w-data.json output/iati-data.json > output/sector-index.json

Started 2021-03 by David Megginson

"""

import json, sys
from .common import * # common variables and functions


index = {}
""" The index that we will export as JSON """


#
# Check command-line usage
#
if len(sys.argv) < 2:
    print("Usage: {} <activity-file...>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)


#
# Loop through the activities in the JSON file specified
#
for filename in sys.argv[1:]:
    with open(filename, "r") as input:
        activities = json.load(input)
        for activity in activities:

            identifier = activity["identifier"]
            source = activity["source"]

            #
            # Loop through the sector types
            #
            for type in SECTOR_TYPES:
                for sector in activity["sectors"][type]:

                    stub = make_token(sector)

                    # Set up this sector's entry (if it doesn't already exist)
                    index.setdefault(type, {})
                    index[type].setdefault(stub, {
                        "name": normalise_string(sector),
                        "type": type,
                        "stub": make_token(sector),
                        "activities": [],
                        "orgs": {
                            "all": {
                                "local": {},
                                "regional": {},
                                "international": {},
                                "unknown": {},
                            },
                            "3w": {
                                "local": {},
                                "regional": {},
                                "international": {},
                                "unknown": {},
                            },
                            "iati": {
                                "local": {},
                                "regional": {},
                                "international": {},
                                "unknown": {},
                            },
                        },
                        "locations": {
                            "all": {
                                "admin1": {},
                                "admin2": {},
                                "unclassified": {},
                            },
                            "3w": {
                                "admin1": {},
                                "admin2": {},
                                "unclassified": {},
                            },
                            "iati": {
                                "admin1": {},
                                "admin2": {},
                                "unclassified": {},
                            },
                        },
                    });
                    entry = index[type][stub]

                    # Add a brief summary of the activity
                    add_unique(activity["identifier"], entry["activities"])

                    # Classify organisations by their scope
                    for role in ROLES:
                        for org_name in activity["orgs"].get(role, []):
                            if org_name:
                                for facet in ("all", source.lower(),):
                                    org = lookup_org(org_name, create=True)
                                    entry["orgs"][facet][org["scope"]].setdefault(org["stub"], 0)
                                    entry["orgs"][facet][org["scope"]][org["stub"]] += 1

                    # locations
                    for loctype in LOCATION_TYPES:
                        for location in activity["locations"].get(loctype, []):
                            if location:
                                for facet in ("all", source.lower(),):
                                    entry["locations"][facet][loctype].setdefault(location, 0)
                                    entry["locations"][facet][loctype][location] += 1

# Dump index to standard output
json.dump(index, sys.stdout, indent=4)
# end
