""" Merge IATI and 3W activities into a single list """

import json, sys

if len(sys.argv) < 2:
    print("Usage: {} <file> [file ...]".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

activities = []

for i, filename in enumerate(sys.argv[1:]):
    with open(filename, "r") as input:
        activities = activities + list(json.load(input))

print(json.dumps(activities))






