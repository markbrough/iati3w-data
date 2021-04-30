import json, sys

from iati3w_common import make_token

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

def get_org_stubs (activity):
    result = set()
    for role in activity["orgs"]:
        for stub in activity["orgs"][role]:
            result.add(stub)
    return result
    
def make_node (org):
    return (org["info"]["shortname"][:32], GROUPS[org["info"]["scope"]],)

def make_link_key (org1, org2):
    return (org1["info"]["shortname"][:32], org2["info"]["shortname"][:32],)


nodes = set()

links = {}
    
for activity in activities.values():

    org_names = sorted(list(get_org_stubs(activity)))
    for i in range(0, len(org_names)):
        org1 = org_index[make_token(org_names[i])]
        for j in range(i + 1, len(org_names)):
            org2 = org_index[make_token(org_names[j])]
            key = make_link_key(org1, org2)
            links[key] = links.get(key, 0) + 1
            nodes.add(make_node(org1))
            nodes.add(make_node(org2))

result = {
    "nodes": [],
    "links": [],
}

for entry in nodes:
    result["nodes"].append({"id": entry[0], "group": entry[1]})

for entry, value in links.items():
    result["links"].append({"source": entry[0], "target": entry[1], "value": value})

json.dump(result, sys.stdout, indent=4)

    
