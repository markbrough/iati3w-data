Data backend for the IATI+3W activity explorer
==============================================

See https://github.com/davidmegginson/iati3w-web/ for the web frontend compontent.

These are Python scripts that will periodically update the data resources for the activity explorer, eventually using GitHub Actions.

## Installation

```
pip install -r requirements.txt
```

## Scripts

### download-data.sh

Download the latest IATI and 3W data to the downloads/ directory.

```
bash download-data.sh
```

### iati3w.activities_iati

Extract the latest IATI data for Somalia, starting 2020-01-01, and print as JSON to standard output:

```
python3 -m iati3w.activities_iati downloads/iati-*.xml > output/iati-data.json
```

### iati3w.activities_3w

Extract the latest 3W data for Somalia, and print as JSON to standard output:

```
python3 -m iati3w.activities_3w downloads/3w-*.csv > output/3w-data.json
```

### iati3w.org_index

Create an index of orgs from the extracted activities:

```
python3 -m iati3w.org_index output/iati-data.json output/3w-data.json > output/org-index.json
```

### iati3w.sector_index

Create an index of sectors from the extracted activities:

```
python3 -m iati3w.sector_index output/iati-data.json output/3w-data.json > output/sector-index.json
```

### iati3w.location_index

Create an index of locations from the extracted activities:

```
python3 -m iati3w.location_index output/iati-data.json output/3w-data.json > output/location-index.json
```

### iati3w.merge

Merge the raw extracted activities into a single file, and resolve unknown orgs/locations.

```
python3 -m iati3w.

## Author

Started by David Megginson.

## License

This software is in the PUBLIC DOMAIN, and comes with no warranty. See UNLICENSE.md for details.

