Data backend for the IATI+3W activity explorer
==============================================

See https://github.com/davidmegginson/iati3w-web/ for the web frontend compontent.

These are Python scripts that will periodically update the data resources for the activity explorer, eventually using GitHub Actions.

## Installation

```
pip install -r requirements.txt
```

## Scripts

### fetch-iati-data.py

Fetch the latest IATI data for Somalia, starting 2020-01-01, and print as JSON to standard output:

```
python3 fetch-iati-data.py > so-iati-activities.json
```

## Author

Started by David Megginson.

## License

This software is in the PUBLIC DOMAIN, and comes with no warranty.

