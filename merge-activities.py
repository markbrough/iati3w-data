""" Merge IATI and 3W activities into a single list """

import json, sys

if len(sys.argv) < 2:
    print("Usage: {} <file> [file ...]".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

result = {}

for i, filename in enumerate(sys.argv[1:]):
    with open(filename, "r") as input:
        activities = json.load(input)
    for activity in activities:
        result.setdefault(activity["identifier"], activity)

print(json.dumps(result))






