""" Print a JSON summary of all IATI activities for Somalia from 2020-01-01 forward """

import diterator, json

#
# Utility functions
#

def classify_local (org_type):
    """ Return True if an org type is local, False if international, or None if ambiguous 
    See https://iatistandard.org/en/iati-standard/203/codelists/organisationtype/

    """
    if org_type in ["24", "72"]:
        return "local"
    elif org_type in ["10", "11", "15", "22", "23", "30", "70", "80", "90"]:
        return "uncertain"
    else:
        return "international"

    
def is_humanitarian_related (activity):
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

print("[")

for i, activity in enumerate(activities):

    data = {
        "source": "IATI",
        "is_humanitarian_related": is_humanitarian_related(activity),
        "identifier": activity.identifier,
        "title": str(activity.title),
        "description": str(activity.description),
        "orgs": [[str(org), classify_local(org.type)] for org in activity.participating_orgs],
        "dac_sectors": [str(sector) for sector in activity.sectors_by_vocabulary.get("1", [])],
        "clusters": [str(sector) for sector in activity.sectors_by_vocabulary.get("10", [])],
        "start_date": activity.start_date_actual if activity.start_date_actual else activity.start_date_planned,
        "end_date": activity.end_date_actual if activity.end_date_actual else activity.end_date_planned,
        "is_active": True if activity.activity_status == "2" else False,
        "locations": list(set([str(location.name) for location in activity.locations if location.name])),
    }
    if i > 0:
        print(",")
    print(json.dumps(data, indent=4), end="")

print("\n]")


# end
