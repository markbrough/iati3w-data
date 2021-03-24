import json, sys

if len(sys.argv) != 2:
    print("Usage: {} <activity-file>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

index = {}

with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for activity in activities:
        for type in ["countries", "admin1", "admin2", "unclassified"]:
            for location in activity["locations"][type]:
                index.setdefault(type, {})
                index[type].setdefault(location, [])
                index[type][location].append({
                    "identifier": activity["identifier"],
                    "title": activity["title"],
                    "orgs": activity["orgs"],
                    "sectors": activity["sectors"],
                })

print(json.dumps(index, indent=4))

