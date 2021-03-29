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
    for activity in activities:

        #
        # Loop through the activity roles
        #
        for role in ROLES:

            #
            # Loop through each org and index it
            #
            for org in activity["orgs"].get(role, []):

                # Skip blank orgs
                if not org:
                    continue

                # Clean whitespace
                org = org.strip();

                # Add a default record if this is the first time we've seen the org
                index.setdefault(org, {
                    "activities": {},
                    "partners": {},
                    "sectors": {},
                    "locations": {},
                    "total_activities": 0,
                })

                # This is the org index entry we'll be working on
                entry = index[org]

                # Count activities
                entry["total_activities"] += 1;

                # Add this activity to the org's index
                entry["activities"].setdefault(role, [])
                entry["activities"][role].append({
                    "identifier": activity["identifier"],
                    "title": activity["title"],
                    "source": activity["source"],
                    "orgs": flatten(activity["orgs"]),
                    "sectors": flatten(activity["sectors"]),
                    "locations": flatten(activity["locations"], excludes=["countries"]),
                })

                # Add the other orgs as partners (don't track roles here)
                for role in ROLES:
                    for partner in activity["orgs"][role]:
                        partner = partner.strip()
                        if partner and (partner != org):
                            entry["partners"].setdefault(partner, 0)
                            entry["partners"][partner] += 1

                # Add the sectors (DAC and Humanitarian)
                for type in SECTOR_TYPES:
                    for sector in activity["sectors"].get(type, []):
                        if sector:
                            entry["sectors"].setdefault(type, {})
                            entry["sectors"][type].setdefault(sector, 0)
                            entry["sectors"][type][sector] += 1

                # Add the subnational locations
                for type in LOCATION_TYPES:
                    for location in activity["locations"].get(type, []):
                        if location:
                            entry["locations"].setdefault(type, {})
                            entry["locations"][type].setdefault(location, 0)
                            entry["locations"][type][location] += 1

# Dump the index to stdout
print(json.dumps(index, indent=4))

# end
