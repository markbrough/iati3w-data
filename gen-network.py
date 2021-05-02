""" Generate a network diagram of connections among orgs """

import json, sys

from iati3w_common import make_token


#
# Step 1: load the org index
#

ORG_INDEX = "output/org-index.json"

with open(ORG_INDEX, "r") as input:
    org_index = json.load(input)


#
# Step 2: gather link data by iterating through the org index
#

links = {}

# iterate through all the orgs we've indexed
for org in org_index.values():

    # skip orgs we're not interested in recording
    if org["info"].get("skip", False):
        continue

    # create a link to every recorded partner org
    for scope in org["partners"].keys():
        for stub in org["partners"][scope]:

            # use > to preserve a predictable order, and avoid partnering orgs with themselves
            if stub > org["info"]["stub"]:
                
                partner = org_index[stub]

                # don't record a link if the partner doesn't exist, or should be skipped
                if partner is None or partner["info"].get("skip", False):
                    continue

                # the key is a tuple of the two stubs
                key = (org["info"]["stub"], partner["info"]["stub"],)

                # TODO: we'll also need to add more info here for filtering
                links[key] = links.get(key, 0) + 1


#
# Step 3: prepare the collected data for the network diagram
#

# result format is a list of nodes and a list of links
result = {
    "nodes": [],
    "links": [],
}

# format the nodes
for stub, org in org_index.items():

    # add extra info about the nodes, for filtering purposes
    result["nodes"].append({
        "stub":stub,
        "name": org["info"]["name"],
        "shortname": org["info"]["shortname"],
        "humanitarian": org["humanitarian"],
        "sources": org["sources"],
        "scope": org["info"]["scope"],
        "sectors": {
            "humanitarian": sorted(org["sectors"].get("humanitarian", {}).keys()),
            "dac": sorted(org["sectors"].get("dac", {}).keys()),
        },
        "admin1": sorted(org["locations"].get("admin1", {}).keys()),
    })

# format the links
for entry, value in links.items():
    result["links"].append({"source": entry[0], "target": entry[1], "value": value})

#
# Step 4: send the result to output
#

json.dump(result, sys.stdout, indent=4)

# end

    
