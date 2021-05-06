""" Generate stats from the input IATI 

Usage:
    python3 iati-stats.py *.xml > stats.json

"""

import diterator, json, sys


def increment_entry (table, *args):
    """ Add 1 to the value for a multi-level entry, creating it if needed

    increment_entry(table, "foo", "bar", "hack")

    will add one to the value of table["foo"]["bar"]["hack"], creating the various levels as needed.
    """
    names = list(args)
    key = names.pop()

    node = table
    for name in names:
        if not name:
            name = None
        node = node.setdefault(name, {})
    node[key] = node.get(key, 0) + 1


def process_files (files):
    """ Process a list of IATI files """

    stats = {}
    activities_seen = set()

    def record_org (org, involvement):
        """ Record an org with or without org id """
        if not org:
            return
        elif org.ref:
            increment_entry(stats, "orgs_with_ref", involvement, org.type)
        else:
            increment_entry(stats, "orgs_without_ref", involvement, org.type)

    # Loop through the IATI XML files from the command line
    for file in files:

        # Loop through the activities in each file
        for activity in diterator.XMLIterator(file):

            # Skip duplicate activities
            identifier = activity.identifier
            if identifier in activities_seen:
                continue
            else:
                activities_seen.add(identifier)

            # Update stats for the reporting org
            record_org(activity.reporting_org, "reporting")

            # Update stats for the participating orgs
            for org in activity.participating_orgs:
                record_org(org, "participating")

            # Update stats for the provider and receiver orgs in each transaction
            for transaction in activity.transactions:
                record_org(transaction.provider_org, "provider")
                record_org(transaction.receiver_org, "receiver")

    return stats

#
# Main entry point
#

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python iati-stats.py <iati-file...>", file=sys.stderr)
        exit(2)
    stats = process_files(sys.argv[1:])
    json.dump(stats, sys.stdout, indent=4)

# end
