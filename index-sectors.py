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
if len(sys.argv) != 2:
    print("Usage: {} <activity-file>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)


#
# Loop through the activities in the JSON file specified
#
with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for activity in activities:

        #
        # Loop through the sector types
        #
        for type in SECTOR_TYPES:
            for sector in activity["sectors"][type]:

                # Set up this sector's entry (if it doesn't already exist)
                index.setdefault(type, {})
                index[type].setdefault(sector, {
                    "activities": [],
                    "orgs": {},
                    "locations": {},
                });
                entry = index[type][sector]

                
                # Add a brief summary of the activity
                entry["activities"].append({
                    "identifier": activity["identifier"],
                    "title": activity["title"],
                    "source": activity["source"],
                    "orgs": flatten(activity["orgs"]),
                    "locations": flatten(activity["locations"], excludes=["countries"]),
                })

                # orgs
                for role in ROLES:
                    for org in activity["orgs"].get(role, []):
                        if org:
                            entry["orgs"].setdefault(org, 0)
                            entry["orgs"][org] += 1

                # locations
                for loctype in LOCATION_TYPES:
                    for location in activity["locations"].get(loctype, []):
                        if location:
                            entry["locations"].setdefault(loctype, {})
                            entry["locations"][loctype].setdefault(location, 0)
                            entry["locations"][loctype][location] += 1

# Dump index to standard output
print(json.dumps(index, indent=4))

# end


