""" Print a JSON summary of all IATI activities for Somalia from 2020-01-01 forward """

import diterator, json, sys

from iati3w_common import *

#
# Utility functions
#

def get_role (org):
    """ Get a text label for an organisation's role in an activity """
    if org.role == "1":
        return "funding"
    elif org.role == "4":
        return "implementing"
    else:
        return "programming"

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


#
# Show all activities from 2020-01-01 forward
#

activities = diterator.Iterator({
    "country_code": "SO",
    "day_end_gteq": "2020-01-01",
})

# We need only basic metadata for each activity
# Print one at a time to keep memory usage low

result = []

for activity in activities:

    org_map = activity.participating_orgs_by_role

    data = {
        "identifier": activity.identifier,
        "source": "IATI",
        "reported_by": str(activity.reporting_org.name),
        "has_humanitarian_content": has_humanitarian_content(activity),
        "title": str(activity.title),
        "description": str(activity.description),
        "is_active": True if activity.activity_status == "2" else False,
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
    }

    # Add orgs
    # FIXME classify by scope
    for params in [["4", "implementing"], ["3", "programming"], ["2", "programming"], ["1", "funding"]]:
        for org in org_map.get(params[0], []):
            info = lookup_org(org.name)
            if info is not None:
                add_unique(info["name"], data["orgs"][params[1]])

    # Look up DAC sectors and humanitarian equivalents
    for vocab in ["1", "2"]:
        for sector in activity.sectors_by_vocabulary.get(vocab, []):
            info = lookup_sector(sector.code)
            if info is not None:
                add_unique(info["dac-group"], data["sectors"]["dac"])
                if "humanitarian-mapping" in info:
                    add_unique(info["humanitarian-mapping"], data["sectors"]["humanitarian"])

    # Look up humanitarian clusters by code
    for sector in activity.sectors_by_vocabulary.get("10", []):
        info = lookup_cluster(sector.code)
        if info is not None:
            add_unique(info["name"], data["sectors"]["humanitarian"])

    # Look up location strings
    for location in activity.locations:
        info = lookup_location(str(location.name))
        if info["level"] == "admin1":
            add_unique(info["name"], data["locations"]["admin1"])
        elif info["level"] == "admin2":
            add_unique(info["name"], data["locations"]["admin2"])
            add_unique(info.get("admin1", None), data["locations"]["admin1"])
        elif info["level"] == "unclassified":
            add_unique(info["name"], data["locations"]["unclassified"])
            add_unique(info.get("admin2", None), data["locations"]["admin2"])
            add_unique(info.get("admin1", None), data["locations"]["admin1"])
    
    result.append(data)

print(json.dumps(result, indent=4))

# end
