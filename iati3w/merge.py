""" Merge IATI and 3W activities into a single object, indexed by identifier.

Usage:

    python3 -m iati3w.merge output/3w-data.json output/iati-data.json > output/activities.json

"""

import json, sys

from .common import *

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: {} <file> [file ...]".format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)

    result = {}

    def clean_activity (activity):
        for role, stub_list in activity["orgs"].items():
            activity["orgs"][role] = [lookup_org(stub, create=True)["stub"] for stub in stub_list]
        for type, stub_list in activity["sectors"].items():
            activity["sectors"][type] = [make_token(stub) for stub in stub_list]
        for level, stub_list in activity["locations"].items():
            activity["locations"][level] = [lookup_location(stub, loctype=level)["stub"] for stub in stub_list]
        return activity

    for i, filename in enumerate(sys.argv[1:]):
        with open(filename, "r") as input:
            activities = json.load(input)
        for activity in activities:
            result.setdefault(activity["identifier"], clean_activity(activity))

    json.dump(result, sys.stdout, indent=4)






