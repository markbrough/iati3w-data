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
            "implementing": list(set([str(org.name) for org in org_map.get("4", [])])),
            "programming": list(set(
                [str(org.name).strip() for org in org_map.get("2", [])] +
                [str(org.name).strip() for org in org_map.get("3", [])]
            )),
            "funding": list(set([str(org.name).strip() for org in org_map.get("1", [])])),
        },
        "sectors": {
            "dac": list(set([sector.code.strip() for sector in activity.sectors_by_vocabulary.get("1", [])])),
            "humanitarian": list(set([sector.code.strip() for sector in activity.sectors_by_vocabulary.get("10", [])])),
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

    # Look up location strings
    for location in activity.locations:
        info = lookup_location(str(location.name))
        loclist = data["locations"][info["level"]]
        if info["name"] not in loclist:
            loclist.append(info["name"])
    
    result.append(data)

print(json.dumps(result, indent=4))

# end
