import json, sys

if len(sys.argv) != 2:
    print("Usage: {} <activity-file>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

index = {}

with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for activity in activities:
        for type in ["dac", "humanitarian"]:
            for sector in activity["sectors"][type]:
                index.setdefault(type, {})
                index[type].setdefault(sector, [])
                index[type][sector].append({
                    "identifier": activity["identifier"],
                    "title": activity["title"],
                    "orgs": activity["orgs"],
                    "locations": activity["locations"],
                })

print(json.dumps(index, indent=4))

