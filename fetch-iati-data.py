""" Print a JSON summary of all IATI activities for Somalia from 2020-01-01 forward """

import diterator, json

def is_local (org_type):
    """ Return True if an org type is local, False if international, or None if ambiguous 
    See https://iatistandard.org/en/iati-standard/203/codelists/organisationtype/

    """
    if org_type in ["11", "24"]:
        return True
    elif org_type in ["15", "22", "23", "90"]:
        return None
    else:
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
        "identifier": activity.identifier,
        "title": str(activity.title),
        "description": str(activity.description),
        "orgs": [[str(org), is_local(org.type)] for org in activity.participating_orgs],
        "dac_sectors": [str(sector) for sector in activity.sectors_by_vocabulary.get("1", [])],
        "clusters": [str(sector) for sector in activity.sectors_by_vocabulary.get("10", [])],
        "start_date": activity.start_date_actual if activity.start_date_actual else activity.start_date_planned,
        "end_date": activity.end_date_actual if activity.end_date_actual else activity.end_date_planned,
        "is_active": True if activity.activity_status == "2" else False,
        "locations": [str(location.name) for location in activity.locations if location.name]
    }
    if i > 0:
        print(",")
    print(json.dumps(data, indent=4), end="")

print("\n]")

# end
