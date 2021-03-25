import json, sys

ROLES = ["implementing", "programming", "funding"]

LOCTYPES = ["admin1", "admin2", "unclassified"]

if len(sys.argv) != 2:
    print("Usage: {} <activity-file>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

def add_to_list (l, items):
    unique_values = set(l)
    for item in items:
        if item:
          unique_values.add(item)
    return sorted(list(unique_values))

index = {}

with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for activity in activities:
        for type in ["dac", "humanitarian"]:
            for sector in activity["sectors"][type]:
                index.setdefault(type, {})
                index[type].setdefault(sector, {
                    "activities": [],
                    "orgs": [],
                    "locations": []
                });

                entry = index[type][sector]

                # activities
                info = {
                    "identifier": activity["identifier"],
                    "title": activity["title"],
                    "orgs": [],
                    "locations": []
                }

                for role in ROLES:
                    info["orgs"] = add_to_list(info["orgs"], activity["orgs"][role])

                for loctype in LOCTYPES:
                    info["locations"] = add_to_list(info["locations"], activity["locations"][loctype])

                entry["activities"].append(info)

                # orgs
                for role in ROLES:
                    entry["orgs"] = add_to_list(entry["orgs"], activity["orgs"].get(role, []))

                # locations
                for loctype in LOCTYPES:
                    entry["locations"] = add_to_list(entry["locations"], activity["locations"].get(loctype, []))

                
print(json.dumps(index, indent=4))

