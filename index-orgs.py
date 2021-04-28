""" Create a JSON index with information about each org in the activities

Usage:

python3 index-orgs.py output/activities.json > output/org-index.json

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
# Loop through all the activities in the JSON file specified
#
with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for identifier, activity in activities.items():

        #
        # Loop through the activity roles
        #
        for role in ROLES:

            #
            # Loop through each org and index it
            #
            for org_name in activity["orgs"].get(role, []):

                # Skip blank orgs
                if is_empty(org_name):
                    continue

                # Add a default record if this is the first time we've seen the org
                index.setdefault(org_name, {
                    "info": lookup_org(org_name, create=True),
                    "sources": [],
                    "humanitarian": False, # change to True if we see a humanitarian activity
                    "activities": {
                        "implementing": [],
                        "programming": [],
                        "funding": [],
                    },
                    "partners": {
                        "local": {},
                        "regional": {},
                        "international": {},
                        "unknown": {},
                    },
                    "sectors": {
                        "humanitarian": {},
                        "dac": {},
                    },
                    "locations": {
                        "admin1": {},
                        "admin2": {},
                        "unclassified": {},
                    },
                    "total_activities": 0,
                })

                # This is the org index entry we'll be working on
                entry = index[org_name]

                # True if we see the org involve in any humanitarian activity
                if activity["humanitarian"]:
                    entry["humanitarian"] = True

                # Note how we know about the org
                add_unique(activity["source"], entry["sources"])

                # Count activities
                entry["total_activities"] += 1;

                # Add this activity to the org's index
                entry["activities"][role].append(activity["identifier"])

                # Add the other orgs as partners (don't track roles here)
                for role in ROLES:
                    for partner in activity["orgs"][role]:
                        if not is_empty(partner) and partner != org_name:
                            org = lookup_org(partner, create=True)
                            entry["partners"][org["scope"]].setdefault(partner, 0)
                            entry["partners"][org["scope"]][partner] += 1

                # Add the sectors (DAC and Humanitarian)
                for type in SECTOR_TYPES:
                    for sector in activity["sectors"].get(type, []):
                        if sector:
                            entry["sectors"][type].setdefault(sector, 0)
                            entry["sectors"][type][sector] += 1

                # Add the subnational locations
                for type in LOCATION_TYPES:
                    for location in activity["locations"].get(type, []):
                        if location:
                            entry["locations"][type].setdefault(location, 0)
                            entry["locations"][type][location] += 1

# Dump the index to stdout
print(json.dumps(index))

# end
