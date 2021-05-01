""" Print a JSON summary of all IATI activities for Somalia from 2020-01-01 forward """

import diterator, json, sys

from iati3w_common import *

#
# Utility functions
#

def has_humanitarian_content (activity):
    """ More-thorough review of an activity to check if it seems humanitarian.
    Will return true if the activity is flagged humanitarian, any transaction
    is flagged humanitarian, a humantarian-scope is present, and/or it
    mentions a humanitarian sector.

    """

    def is_humanitarian_sector (sector):
        """ Check if a sector is humanitarian """
        if sector.vocabulary == "10":
            # humanitarian clusters
            return True
        elif sector.vocabulary in ["1", "2"] and sector.code.startswith("7"):
            # DAC humanitarian sectors
            return True
        else:
            return False
          
    
    if activity.humanitarian or len(activity.humanitarian_scopes) > 0:
        return True

    for sector in activity.sectors:
        if is_humanitarian_sector(sector):
            return True

    for transaction in activity.transactions:
        if transaction.humanitarian:
            return True
        for sector in transaction.sectors:
            if is_humanitarian_sector(sector):
                return True
        
    return False

def add_org (org, role, data):
    """ Add an org to the appropriate list """
    #  the name here instead of the stub if the org isn't in the org map
    # lookup_org() will recreate the record for index-orgs.py, which
    # will switch to the stub
    if org is None or org.get("skip", False):
        return
    key = "name" if org.get("unrecognised", False) else "stub"
    add_unique(org[key], data["orgs"][role])


#
# Lookup tables
#

def lookup_sector (code):
    """ Look up a DAC purpose by 3-digit code """
    map = get_dataset("inputs/dac3-sector-map.json")
    return map.get(code[:3], None) # use the 3-digit code

def lookup_cluster (code):
    """ Look up a humanitarian cluster by code """
    map = get_dataset("inputs/humanitarian-cluster-map.json")
    return map.get(code, None)


def make_activity(activity):

    org_map = activity.participating_orgs_by_role

    data = {
        "identifier": activity.identifier,
        "source": "IATI",
        "reported_by": None,
        "humanitarian": has_humanitarian_content(activity),
        "title": str(activity.title),
        "description": str(activity.description),
        "active": True if activity.activity_status == "2" else False,
        "orgs": {
            "implementing": [],
            "programming": [],
            "funding": [],
        },
        "sectors": {
            "dac": [],
            "humanitarian": [],
        },
        "locations": {
            "unclassified": [],
            "admin2": [],
            "admin1": [],
            "countries": [country.code.upper() for country in activity.recipient_countries],
        },
        "dates": {
            "start": activity.start_date_actual if activity.start_date_actual else activity.start_date_planned,
            "end": activity.end_date_actual if activity.end_date_actual else activity.end_date_planned
        },
        "modalities": [], # TODO
        "targeted": {}, # TODO
    }

    reporting_org = lookup_org(activity.reporting_org.ref, create=False) or lookup_org(str(activity.reporting_org.name), create=True)
    if reporting_org is not None:
        key = "name" if reporting_org.get("unrecognised", False) else "stub"
        data["reported_by"] = reporting_org[key]

    # Add orgs
    for params in [
            ["4", "implementing"],
            ["3", "programming"],
            ["2", "programming"],
            ["1", "funding"]
    ]:
        for org in org_map.get(params[0], []):
            info = lookup_org(org.ref) or lookup_org(org.name, create=True)
            if info is not None and not info.get("skip", False):
                add_org(info, params[1], data)

    # Add any extra orgs from transactions
    for transaction in activity.transactions:
        def try_org (org, type):
            if org is not None:
                info = lookup_org(org.ref) or lookup_org(org.name, create=True)
                if info is not None:
                    add_org(info, type, data)
        if transaction.type in ("1", "2", "3", "11"):
            try_org(transaction.receiver_org, "implementing")
            try_org(transaction.provider_org, "funding")

    # Look up DAC sectors and humanitarian equivalents
    for vocab in ["1", "2"]:
        for sector in activity.sectors_by_vocabulary.get(vocab, []):
            info = lookup_sector(sector.code)
            if info is not None and not info.get("skip", False):
                add_unique(info["dac-group"], data["sectors"]["dac"])
                if "humanitarian-mapping" in info:
                    add_unique(info["humanitarian-mapping"], data["sectors"]["humanitarian"])

    # Look up humanitarian clusters by code
    for sector in activity.sectors_by_vocabulary.get("10", []):
        info = lookup_cluster(sector.code)
        if info is not None and not info.get("skip", False):
            add_unique(info["name"], data["sectors"]["humanitarian"])

    # Look up location strings
    for location in activity.locations:
        if location.name is None or is_empty(str(location.name)):
            continue
        info = lookup_location(str(location.name))

        # honour the "skip" flag
        if info is None or info.get("skip", False):
            continue

        # Add the name here instead of the stub if the org isn't in the map
        # lookup_org() will recreate the record for index-orgs.py, which
        # will switch to the stub
        key = "name" if info.get("unrecognised", False) else "stub"
        add_unique(info[key], data["locations"][info["level"]])

        #
        # Add the ancestor admin1 and admin2 if they exist
        for level in ["admin1", "admin2"]:
            if level in info:
                add_unique(info[level], data["locations"][level])

    # There must be at list one sector left to count this activity
    if len(data["sectors"]["humanitarian"]) + len(data["sectors"]["dac"]) > 0:
        return data
    else:
        return None

def fetch_activities(files):

    result = []
    identifiers_seen = set()

    for file in files:
        with open(file, "r") as input:
            for activity in diterator.XMLIterator(input):
                if not activity.identifier in identifiers_seen:
                    data = make_activity(activity)
                    if data is not None:
                        result.append(data)
                    identifiers_seen.add(activity.identifier)

    return result

#
# Script entry point
#
if __name__ == "__main__":
    data = fetch_activities(sys.argv[1:])
    print("Found {} IATI activities".format(len(data)), file=sys.stderr)
    json.dump(data, sys.stdout, indent=4)

# end
