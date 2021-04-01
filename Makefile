########################################################################
# This Makefile will (re)build all JSON data files as needed
#
# Usage:
#
#   $ make all         # rebuild only what's out of date
#   $ make force all   # force everything to rebuild, e.g. in a cronjob
#
# The process will stop with an error code if any part of it fails
#
# Started 2021-03 by David Megginson
########################################################################

#
# Variables
#

# Python virtual environment
VENV=venv/bin/activate

# Target files
TIMESTAMP=output/timestamp
IATI_ACTIVITIES=output/iati-data.json
3W_ACTIVITIES=output/3w-data.json
ACTIVITIES=output/activities.json
ORG_INDEX=output/org-index.json
SECTOR_INDEX=output/sector-index.json
LOCATION_INDEX=output/location-index.json

# Supporting map files
MAPS=inputs/dac3-sector-map.json inputs/humanitarian-cluster-map.json inputs/location-map.json inputs/org-map.json

#
# Convenience targets
#

all: index

push-update: index
	cd output && git add . && git commit -m "Data update" && git push origin

index: index-orgs index-sectors index-locations

index-orgs: $(ORG_INDEX)

index-sectors: $(SECTOR_INDEX)

index-locations: $(LOCATION_INDEX)

merge-activities: $(ACTIVITIES)

fetch-iati: $(IATI_ACTIVITIES)

fetch-3w: $(3W_ACTIVITIES)


#
# File targets
#

$(ORG_INDEX): venv $(ACTIVITIES) index-orgs.py
	. $(VENV) && python index-orgs.py $(ACTIVITIES) > $@

$(SECTOR_INDEX): venv $(ACTIVITIES) index-sectors.py iati3w_common.py
	. $(VENV) && python index-sectors.py $(ACTIVITIES) > $@

$(LOCATION_INDEX): venv $(ACTIVITIES) index-locations.py iati3w_common.py
	. $(VENV) && python index-locations.py $(ACTIVITIES) > $@

$(ACTIVITIES): venv $(IATI_ACTIVITIES) $(3W_ACTIVITIES) merge-activities.py iati3w_common.py
	. $(VENV) && python merge-activities.py $(IATI_ACTIVITIES) $(3W_ACTIVITIES) > $@

$(IATI_ACTIVITIES): venv fetch-iati-data.py iati3w_common.py $(MAPS) $(TIMESTAMP)
	. $(VENV) && mkdir -p output && python fetch-iati-data.py > $@

$(3W_ACTIVITIES): venv fetch-3w-data.py iati3w_common.py $(MAPS) $(TIMESTAMP)
	. $(VENV) && mkdir -p output && python fetch-3w-data.py > $@


#
# Extras
#

# Create the timestamp file if it's missing
$(TIMESTAMP):
	touch $(TIMESTAMP)

# Create the Python3 virtual environment
venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

# Delete the timestamp and force a complete build
force:
	touch $(TIMESTAMP)
