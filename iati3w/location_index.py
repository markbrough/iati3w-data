""" Create a JSON index with information about each location in the activities

Usage:

    python3 -m iati3w.location_index output/3w-data.json output/iati-data.json > output/location-index.json

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
# Loop through all the activities in the JSON file specified
#
for filename in sys.argv[1:]:
    with open(filename, "r") as input:

        activities = json.load(input)
        for activity in activities:

            identifier = activity["identifier"]
            source = activity["source"]

            #
            # Loop through the subnational location types
            #
            for loctype in LOCATION_TYPES:

                # Add the type if it's not in the index yet
                index.setdefault(loctype, {})

                #
                # Loop through each location of each type
                #
                for locname in activity["locations"].get(loctype, []):

                    location = lookup_location(locname)

                    if not location or location.get("skip", False):
                        continue

                    # Add a default record if this is the first time we've seen the location
                    index[loctype].setdefault(location["stub"], {
                        "info": location,
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
                        "sectors": {
                            "all": {
                                "humanitarian": {},
                                "dac": {},
                            },
                            "3w": {
                                "humanitarian": {},
                                "dac": {},
                            },
                            "iati": {
                                "humanitarian": {},
                                "dac": {},
                            },
                        },
                    })

                    # This is the location index entry we'll be working on
                    entry = index[loctype][location["stub"]]

                    # Add this activity
                    entry["activities"].append(activity["identifier"])

                    # Add the activity orgs (don't track roles here)
                    for role in ROLES:
                        for org_name in activity["orgs"].get(role, []):
                            if not org_name:
                                continue
                            org = lookup_org(org_name, create=True)
                            for facet in ("all", source.lower(),):
                                entry["orgs"][facet][org["scope"]].setdefault(org["stub"], 0)
                                entry["orgs"][facet][org["scope"]][org["stub"]] += 1

                    # Add the sectors for each type
                    for type in SECTOR_TYPES:
                        for sector in activity["sectors"].get(type, []):
                            if not sector:
                                continue
                            stub = make_token(sector)
                            for facet in ("all", source.lower(),):
                                entry["sectors"][facet][type].setdefault(stub, 0)
                                entry["sectors"][facet][type][stub] += 1


# Dump the index as JSON to stdout
json.dump(index, sys.stdout, indent=4)

# end

