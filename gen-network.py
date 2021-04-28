import json, sys

ACTIVITIES = "output/activities.json"
ORG_INDEX = "output/org-index.json"

GROUPS = {
    "local": 1,
    "regional": 2,
    "international": 3,
    "unknown": 4,
}

with open(ACTIVITIES, "r") as input:
    activities = json.load(input)

with open(ORG_INDEX, "r") as input:
    org_index = json.load(input)


nodes = set()
links = {}
    
for activity in activities.values():

    # Get all the orgs in the activity
    org_names = set()
    for type, names in activity["orgs"].items():
        for name in names:
            org_names.add(name)
            org = org_index[name]
            nodes.add((name, GROUPS[org["info"]["scope"]],))

    org_names = sorted(list(org_names))
    for i in range(0, len(org_names)):
        for j in range(i + 1, len(org_names)):
            key = (org_names[i], org_names[j],)
            links[key] = links.get(key, 0) + 1

result = {
    "nodes": [],
    "links": [],
}

for entry in nodes:
    result["nodes"].append({"id": entry[0], "group": entry[1]})

for entry, value in links.items():
    result["links"].append({"source": entry[0], "target": entry[1], "value": value})

json.dump(result, sys.stdout, indent=4)

    
