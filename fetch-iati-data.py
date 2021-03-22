f""" Print a JSON summary of all IATI activities for Somalia from 2020-01-01 forward """

import diterator, json

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

print("[")

for i, activity in enumerate(activities):

    org_map = activity.participating_orgs_by_role

    data = {
        "identifier": activity.identifier,
        "source": "IATI",
        "reported_by": str(activity.reporting_org.name),
        "has_humanitarian_content": has_humanitarian_content(activity),
        "title": str(activity.title),
        "description": str(activity.description),
        "orgs": {
            "implementing": list(set([str(org.name) for org in org_map.get("4", [])])),
            "programming": list(set(
                [str(org.name) for org in org_map.get("2", [])] +
                [str(org.name) for org in org_map.get("3", [])]
            )),
            "funding": list(set([str(org.name) for org in org_map.get("1", [])])),
        },
        "dac_sectors": list(set([sector.code for sector in activity.sectors_by_vocabulary.get("1", [])])),
        "humanitarian_clusters": list(set([str(sector.narrative) for sector in activity.sectors_by_vocabulary.get("10", [])])),
        "start_date": activity.start_date_actual if activity.start_date_actual else activity.start_date_planned,
        "end_date": activity.end_date_actual if activity.end_date_actual else activity.end_date_planned,
        "is_active": True if activity.activity_status == "2" else False,
        "recipient_countries": [country.code.upper() for country in activity.recipient_countries],
        "locations": list(set([str(location.name) for location in activity.locations if location.name])),
    }
    if i > 0:
        print(",")
    print(json.dumps(data, indent=4), end="")

print("\n]")


# end
