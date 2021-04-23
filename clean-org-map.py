import json, re, sys

from iati3w_common import *

def clean_entry(entry):
    info = re.search(r'^(.+) \((.+)\)$', entry["name"])
    if info:
        entry["name"] = normalise_string(info.group(1))
        entry["shortname"] = normalise_string(info.group(2))
        add_unique("{} ({})".format(entry["name"], entry["shortname"]), entry["synonyms"])
    else:
        entry["shortname"] = entry["name"]
    entry["synonyms"] = sorted(list(set(entry.setdefault("synonyms", []))))
    return entry

result = {}

with open("inputs/org-map.json", "r") as input:
    org_map = json.load(input)

for key in sorted(org_map.keys()):
    entry = clean_entry(org_map[key])
    if entry["shortname"] in result:
        print("*** Duplicate entry: {}".format(entry["shortname"]), file=sys.stderr)
        exit(1)
    else:
        result[entry["shortname"]] = entry

print(json.dumps(result, indent=4))

