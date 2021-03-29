""" Show unique top-level keys in a JSON object, sorted

For debugging/testing

"""

import json, sys

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Usage: {} <json-file>".format(sys.argv[0]))
    sys.exit(2)

with open(sys.argv[1], "r") as input:
    data = json.load(input)
    if len(sys.argv) == 3:
        data = data.get(sys.argv[2])
    print(json.dumps(sorted(data.keys()), indent=4))
