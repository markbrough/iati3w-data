import json, sys

ROLES = ["implementing", "programming", "funding"]

LOCTYPES = ["admin1", "admin2", "unclassified"]

if len(sys.argv) != 2:
    print("Usage: {} <activity-file>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

index = {}

with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for activity in activities:
        for type in ["dac", "humanitarian"]:
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
                })

                # orgs
                for role in ROLES:
                    for org in activity["orgs"].get(role, []):
                        if org:
                            entry["orgs"].setdefault(org, 0)
                            entry["orgs"][org] += 1

                # locations
                for loctype in LOCTYPES:
                    for location in activity["locations"].get(loctype, []):
                        if location:
                            entry["locations"].setdefault(location, 0)
                            entry["locations"][location] += 1
                
print(json.dumps(index, indent=4))

