""" Create a JSON index with information about each sector in the activities

Usage:

python3 index-sectors.py output/activities.json > output/sector-index.json

Started 2021-03 by David Megginson

"""

import json, sys
from iati3w_common import * # common variables and functions


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
                            "local": {},
                            "regional": {},
                            "international": {},
                            "unknown": {},
                        },
                        "locations": {
                            "admin1": {},
                            "admin2": {},
                            "unclassified": {},
                        },
                    });
                    entry = index[type][stub]

                    # Add a brief summary of the activity
                    add_unique(activity["identifier"], entry["activities"])

                    # Classify organisations by their scope
                    for role in ROLES:
                        for org_name in activity["orgs"].get(role, []):
                            if org_name:
                                org = lookup_org(org_name, create=True)
                                entry["orgs"][org["scope"]].setdefault(org["stub"], 0)
                                entry["orgs"][org["scope"]][org["stub"]] += 1

                    # locations
                    for loctype in LOCATION_TYPES:
                        for location in activity["locations"].get(loctype, []):
                            if location:
                                entry["locations"][loctype].setdefault(location, 0)
                                entry["locations"][loctype][location] += 1

# Dump index to standard output
json.dump(index, sys.stdout, indent=4)
# end
