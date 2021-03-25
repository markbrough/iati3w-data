import json, sys

ROLES = ["implementing", "programming", "funding"]
SECTOR_TYPES = ["dac", "humanitarian"]
LOCATION_TYPES = ["admin1", "admin2", "unclassified"]

if len(sys.argv) != 2:
    print("Usage: {} <activity-file>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(2)

index = {}

with open(sys.argv[1], "r") as input:
    activities = json.load(input)
    for activity in activities:

        for role in ROLES:
            for org in activity["orgs"][role]:

                # Skip blank orgs
                if not org:
                    continue

                org = org.strip();

                # Add a default record if missing
                index.setdefault(org, {
                    "activities": {},
                    "partners": {},
                    "sectors": {},
                    "locations": {},
                })

                # Index activities
                index[org]["activities"].setdefault(role, [])
                index[org]["activities"][role].append({
                    "identifier": activity["identifier"],
                    "title": activity["title"],
                })

                # Index partners
                for role in ROLES:
                    for partner in activity["orgs"][role]:
                        if partner and (partner != org):
                            index[org]["partners"].setdefault(partner, 0)
                            index[org]["partners"][partner] += 1

                # Index sectors
                for type in SECTOR_TYPES:
                    for sector in activity["sectors"][type]:
                        if sector:
                            index[org]["sectors"].setdefault(sector, 0)
                            index[org]["sectors"][sector] += 1

                # Index locations
                for type in LOCATION_TYPES:
                    for location in activity["locations"][type]:
                        if location:
                            index[org]["locations"].setdefault(location, 0)
                            index[org]["locations"][location] += 1

print(json.dumps(index, indent=4))

