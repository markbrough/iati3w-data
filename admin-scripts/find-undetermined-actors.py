import csv, json, sys

with open("output/org-index.json", "r") as input:
    data = json.load(input)

orgs = []

for key, entry in data.items():
    if entry["info"]["scope"] == "unknown":
        count = 0
        for type, activities in entry["activities"].items():
            count += len(activities)
        orgs.append([entry["info"]["name"], count])

orgs = sorted(orgs, key=lambda entry: entry[1], reverse=True)

#sys.stdout.reconfigure(encoding='utf-8')
output = csv.writer(sys.stdout)
output.writerow(["Org", "activities"])

for row in orgs:
    output.writerow(row)
