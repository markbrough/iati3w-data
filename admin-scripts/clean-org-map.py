import json, re, sys

from iati3w_common import *

def clean_entry(entry):
    entry["synonyms"] = sorted(list(set(entry.setdefault("synonyms", []))))
    if "iati" in entry:
        if entry["iati"]["code"] in entry["synonyms"]:
            entry["synonyms"].remove(entry["iati"]["code"])
        entry["iati_id"] = entry["iati"]["code"]
    return entry

result = {}

with open("inputs/org-map.json", "r") as input:
    org_map = json.load(input)

for key in sorted(org_map.keys()):
    entry = clean_entry(org_map[key])
    if key != entry["shortname"] and entry["shortname"] in result:
        print("*** Duplicate entry: {} | {}".format(entry["shortname"], entry["name"]), file=sys.stderr)
        exit(1)
    else:
        result[entry["shortname"]] = entry

print(json.dumps(result, indent=4))

