Data backend for the IATI+3W activity explorer
==============================================

See https://github.com/davidmegginson/iati3w-web/ for the web frontend compontent.

These are Python scripts that will periodically update the data resources for the activity explorer, eventually using GitHub Actions.

## Installation

```
$ pip install -r requirements.txt
```

## Scripts

On a Unix-like system, you can run the whole processing pipeline simply by entering

```
$ make
```

in the root of the distribution. The information below is for anyone who wants to call the individual components directly.

### admin-scripts/download-data.sh

Download the latest IATI and 3W data to the downloads/ directory.

```
$ bash admin-scripts/download-data.sh
```

### iati3w.activities_iati

Extract the latest IATI data for Somalia, starting 2020-01-01, and print as JSON to standard output:

```
(venv)$ python3 -m iati3w.activities_iati downloads/iati-*.xml > output/iati-data.json
```

Sample output: https://davidmegginson.github.io/iati3w-data/iati-data.json

### iati3w.activities_3w

Extract the latest 3W data for Somalia, and print as JSON to standard output:

```
(venv)$ python3 -m iati3w.activities_3w downloads/3w-*.csv > output/3w-data.json
```

Sample output: https://davidmegginson.github.io/iati3w-data/3w-data.json

### iati3w.org_index

Create an index of orgs from the extracted activities:

```
(venv)$ python3 -m iati3w.org_index output/iati-data.json output/3w-data.json > output/org-index.json
```

Sample output: https://davidmegginson.github.io/iati3w-data/org-index.json

### iati3w.sector_index

Create an index of sectors from the extracted activities:

```
(venv)$ python3 -m iati3w.sector_index output/iati-data.json output/3w-data.json > output/sector-index.json
```

Sample output: https://davidmegginson.github.io/iati3w-data/sector-index.json

### iati3w.location_index

Create an index of locations from the extracted activities:

```
(venv)$ python3 -m iati3w.location_index output/iati-data.json output/3w-data.json > output/location-index.json
```

Sample output: https://davidmegginson.github.io/iati3w-data/location-index.json

### iati3w.merge

Merge the raw extracted activities into a single file, and resolve unknown orgs/locations.

```
(venv)$ python3 -m iati3w.
```

Sample output: https://davidmegginson.github.io/iati3w-data/activities.json

## Methodology notes

### Name matching

IATI data sometimes has organisation identifiers, but almost never has subnational location codes.

3W data usually has subnational location codes (though, strangely, not in the case of the Somalia 3W), but never has organisation identifiers.

As a result, there's a large amount of string-matching necessary to come up with useable data about aid organisations in Somalia, and the sectors and locations where they work. The code uses these two maps to look up synonyms, and uses a string-matching algorithm that ignores character case, whitespace, and puncutation.

Organisation-matching map: [inputs/org-map.json](inputs/org-map.json)

Location-matching map: [inputs/location-map.json](inputs/location-map.json)

### Sector mapping

The scripts map all DAC3 and DAC5 purpose codes in IATI data to the higher-level OECD DAC groups, using [inputs/dac3-sector-map.json](inputs/dac3-sector-map.json). That table also includes mappings from DAC sectors to humanitarian clusters, so that we can assign more IATI activities to the same clusters as 3W activities. You can find all of the mappings in the file.

## Credits

Started by David Megginson, on behalf of Development Initiatives. Thank you to the Netherlands Ministry of Foreign Affairs for their generous support.

## License

This software is in the PUBLIC DOMAIN, and comes with no warranty. See UNLICENSE.md for details.

