########################################################################
# This Makefile will (re)build all JSON data files as needed
#
# Usage:
#
#   $ make all         # rebuild only what's out of date
#   $ make clean all   # force everything to rebuild, e.g. in a cronjob
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
IATI_ACTIVITIES=output/iati-data.json
3W_ACTIVITIES=output/3w-data.json
ACTIVITIES=output/activities.json
ORG_INDEX=output/org-index.json
SECTOR_INDEX=output/sector-index.json
LOCATION_INDEX=output/location-index.json

# Supporting map files
MAPS=inputs/dac3-sector-map.json inputs/humanitarian-cluster-map.json inputs/location-map.json inputs/org-map.json

# Downloaded files (just include the first IATI one)
DOWNLOADS=downloads/3w-som.csv downloads/iati-som-00100.xml

#
# Convenience targets
#

all: index

push-update: index
	cd output && git add . && git commit -m "Data update" && git push origin

index: index-orgs index-sectors index-locations merge-activities

index-orgs: $(ORG_INDEX)

index-sectors: $(SECTOR_INDEX)

index-locations: $(LOCATION_INDEX)

merge-activities: $(ACTIVITIES)

fetch-iati: $(IATI_ACTIVITIES)

fetch-3w: $(3W_ACTIVITIES)

.DELETE_ON_ERROR:


#
# File targets
#

$(ACTIVITIES): venv $(IATI_ACTIVITIES) $(3W_ACTIVITIES) iati3w/merge.py iati3w/common.py
	. $(VENV) && time python -m iati3w.merge $(IATI_ACTIVITIES) $(3W_ACTIVITIES) > $@

$(ORG_INDEX): venv $(IATI_ACTIVITIES) $(3W_ACTIVITIES) iati3w/org_index.py
	. $(VENV) && time python -m iati3w.org_index $(IATI_ACTIVITIES) $(3W_ACTIVITIES) > $@

$(SECTOR_INDEX): venv $(IATI_ACTIVITIES) $(3W_ACTIVITIES) iati3w/sector_index.py iati3w/common.py
	. $(VENV) && time python -m iati3w.sector_index $(IATI_ACTIVITIES) $(3W_ACTIVITIES) > $@

$(LOCATION_INDEX): venv $(IATI_ACTIVITIES) $(3W_ACTIVITIES) iati3w/location_index.py iati3w/common.py
	. $(VENV) && time python -m iati3w.location_index $(IATI_ACTIVITIES) $(3W_ACTIVITIES) > $@

$(IATI_ACTIVITIES): venv iati3w/activities_iati.py iati3w/common.py $(MAPS) $(DOWNLOADS)
	. $(VENV) && mkdir -p output && time python -m iati3w.activities_iati downloads/iati*.xml > $@

$(3W_ACTIVITIES): venv iati3w/activities_3w.py iati3w/common.py $(MAPS) $(DOWNLOADS)
	. $(VENV) && mkdir -p output && time python -m iati3w.activities_3w downloads/3w*.csv > $@

$(DOWNLOADS): download-data.sh
	bash download-data.sh


#
# Extras
#

# Create the Python3 virtual environment
venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

tags: TAGS

TAGS: *.py
	etags *.py

# Clean everything out to force a rebuild
clean:
	rm -rfv venv/
	rm -rfv downloads/
	rm -fv output/*
