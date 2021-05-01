""" Generate a network diagram of connections among orgs """

import json, sys

from iati3w_common import make_token

ORG_INDEX = "output/org-index.json"

with open(ORG_INDEX, "r") as input:
    org_index = json.load(input)

orgs_seen = set()

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
                key = (org["info"]["stub"], partner["info"]["stub"],)
                links[key] = links.get(key, 0) + 1
                orgs_seen.add(org["info"]["stub"])
                orgs_seen.add(partner["info"]["stub"])


result = {
    "nodes": [],
    "links": [],
}

for stub in orgs_seen:
    org = org_index[stub]
    result["nodes"].append({
        "stub":stub,
        "name": org["info"]["name"],
        "shortname": org["info"]["shortname"],
        "scope": org["info"]["scope"],
    })

for entry, value in links.items():
    result["links"].append({"source": entry[0], "target": entry[1], "value": value})

json.dump(result, sys.stdout, indent=4)

    
