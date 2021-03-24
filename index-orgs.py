import json, sys

if len(sys.argv) != 2:
    print("Usage: {} <activity-file>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

index = {}

with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for activity in activities:
        for role in ["implementing", "programming", "funding"]:
            for org in activity["orgs"][role]:
                index.setdefault(org, {})
                index[org].setdefault(role, [])
                index[org][role].append({
                    "identifier": activity["identifier"],
                    "title": activity["title"],
                    "sectors": activity["sectors"],
                    "locations": activity["locations"],
                })

print(json.dumps(index, indent=4))

