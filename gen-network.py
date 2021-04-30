""" Generate a network diagram of connections among orgs """

import json, sys

from iati3w_common import make_token

ORG_INDEX = "output/org-index.json"

GROUPS = {
    "local": 1,
    "regional": 2,
    "international": 3,
    "unknown": 4,
}

with open(ORG_INDEX, "r") as input:
    org_index = json.load(input)

def make_node (org):
    return (org["info"]["shortname"][:32], GROUPS[org["info"]["scope"]],)

def make_link_key (org1, org2):
    return (org1["info"]["shortname"][:32], org2["info"]["shortname"][:32],)


nodes = set()

links = {}
    
for org in org_index.values():

    if org["info"].get("skip", False):
        continue

    for scope in org["partners"].keys():
        for stub in org["partners"][scope]:
            if stub > org["info"]["stub"]:
                partner = org_index[stub]
                if partner is None or partner["info"].get("skip", False):
                    continue
                key = make_link_key(org, partner)
                links[key] = links.get(key, 0) + 1
                nodes.add(make_node(org))
                nodes.add(make_node(partner))


result = {
    "nodes": [],
    "links": [],
}

for entry in nodes:
    result["nodes"].append({"id": entry[0], "group": entry[1]})

for entry, value in links.items():
    result["links"].append({"source": entry[0], "target": entry[1], "value": value})

json.dump(result, sys.stdout, indent=4)

    
