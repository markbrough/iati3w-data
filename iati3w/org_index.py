""" Create a JSON index with information about each org in the activities

Usage:

    python3 -m iati3w.org_index output/3w-data.json output/iati-data.json > output/org-index.json

Started 2021-03 by David Megginson

"""

import copy, json, sys
from .common import * # common variables and functions

TEMPLATE = {
    "info": None,
    "sources": [],
    "humanitarian": False,
    "activities": {
        "implementing": [],
        "programming": [],
        "funding": [],
    },
    "partners": {
        "all": {
            "local": {},
            "regional": {},
            "international": {},
            "unknown": {}
        },
        "3w": {
            "local": {},
            "regional": {},
            "international": {},
            "unknown": {}
        },
        "iati": {
            "local": {},
            "regional": {},
            "international": {},
            "unknown": {}
        },
    },
    "sectors": {
        "humanitarian": {},
        "dac": {},
    },
    "locations": {
        "admin1": {},
        "admin2": {},
        "unclassified": {},
    },
    "total_activities": 0,
}


index = {}
""" The index that we will export as JSON """

#
# Utility functions
#

def get_entry (org):
    """ Return the index entry for an org, creating the entry if necessary """
    global index

    if org is None:
        return None

    stub = org["stub"]
    if not stub in index:
        index[stub] = copy.deepcopy(TEMPLATE)
        index[stub]["info"] = org

    return index[stub]

def add_partner (org, partner, source):
    """ Record one org as a partner of another
    The function works only one way, so you need to call it twice
    """
    
    global index

    # we need two different orgs
    if org is None or partner is None or org["stub"] == partner["stub"] or org.get("skip", False) or partner.get("skip", False):
        return

    stub = partner["stub"]
    basedata = get_entry(org)["partners"]["all"][partner["scope"]]
    basedata[stub] = 1 + basedata.get(stub, 0)

    basedata = get_entry(org)["partners"][source.lower()][partner["scope"]]
    basedata[stub] = 1 + basedata.get(stub, 0)

if __name__ == "__main__":

    #
    # Check command-line usage
    #
    if len(sys.argv) < 2:
        print("Usage: {} <activity-file...>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)

    #
    # Loop through all the activities in the JSON file specified
    #
    for filename in sys.argv[1:]:
        with open(filename, "r") as input:
            activities = json.load(input)
            for activity in activities:

                identifier = activity["identifier"]

                # Make sure we have an entry for the reporting org
                reporting_org = lookup_org(activity["reported_by"], create=True)
                get_entry(reporting_org)

                #
                # Loop through the activity roles
                #
                for role in ROLES:

                    #
                    # Loop through each org and index it
                    #
                    for org_name in activity["orgs"].get(role, []):

                        # The org we're working on
                        org = lookup_org(org_name, create=True)
                        if org is None or org.get("skip", False):
                            continue

                        # This is the org index entry we'll be working on
                        entry = get_entry(org)

                        # True if we see the org involved in any humanitarian activity
                        if activity["humanitarian"]:
                            entry["humanitarian"] = True

                        # Note how we know about the org
                        add_unique(activity["source"], entry["sources"])

                        # Count activities
                        entry["total_activities"] += 1;

                        # Add this activity to the org's index
                        add_unique(activity["identifier"], entry["activities"][role])

                        # Add the reporting org as a partner
                        add_partner(org, reporting_org, activity["source"])
                        add_partner(reporting_org, org, activity["source"])

                        # Add the sectors (DAC and Humanitarian)
                        for type in SECTOR_TYPES:
                            for sector in activity["sectors"].get(type, []):
                                stub = make_token(sector)
                                if sector:
                                    entry["sectors"][type].setdefault(stub, 0)
                                    entry["sectors"][type][stub] += 1

                        # Add the subnational locations
                        for type in LOCATION_TYPES:
                            for location in activity["locations"].get(type, []):
                                if location:
                                    entry["locations"][type].setdefault(location, 0)
                                    entry["locations"][type][location] += 1

    # Dump the index to stdout
    json.dump(index, sys.stdout, indent=4)

# end
