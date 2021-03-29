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

### fetch-3w-data.py

Fetch the latest 3W data for Somalia, and print as JSON to standard output:

```
python3 fetch-iati-data.py > so-iati-activities.json
```

## Output format

Both the IATI and 3W follow similar formats, with a JSON list of objects.

### Sample 3W JSON object

Note that identifiers for 3W activities are just hashes, and are not guaranteed to be stable.

```
{
    "identifier": "90f016202193360e3f1b20765b9989cc2eb1dfd48420fde428d20a0c99e52abd",
    "source": "Somalia 3W",
    "reported_by": "OCHA Somalia",
    "has_humanitarian_content": true,
    "title": "Integrated WASH, Shelter, CCCM, Protection and information management support to improve living conditions of crisis-affected rural and IDP populations in Somalia",
    "description": "CCCM respnse comprised of coordination, monitoring, creation of CMCs, training of CMC, information management at site level, site maintenance. Shetler component (transitional shelters plus ESK) and Protection component ",
    "is_active": true,
    "orgs": {
        "implementing": [
            "SADO"
        ],
        "programming": [
            "ACTED"
        ],
        "funding": []
    },
    "sectors": {
        "dac": [],
        "humanitarian": [
            "CCCM"
        ]
    },
    "locations": {
        "countries": [
            "SO"
        ],
        "admin1": [
            "Lower Juba"
        ],
        "admin2": [
            "Kismayo"
        ],
        "unclassified": [
            "Galbeedt Area "
        ]
    },
    "dates": {
        "start": "2020-09-01",
        "end": "2021-02-28"
    }
}
```

### Sample IATI JSON object

Note that the majority of IATI records will not have humanitarian content and will not list humanitarian clusters. Unlike 3W activities, IATI activities will sometimes list multiple countries, and will nearly always list DAC sectors (which are always empty in the 3W objects).


```
{
    "identifier": "XM-DAC-41121-2020-EHGL-SOM",
    "source": "IATI",
    "reported_by": "United Nations High Commissioner for Refugees (UNHCR)",
    "has_humanitarian_content": true,
    "title": "UNHCR operation in Somalia (2020)",
    "description": "This activity shows details of the UNHCR operation in Somalia for 2020 including the budget, funding, expenditure and results.",
    "is_active": false,
    "orgs": {
        "implementing": [
            "United Nations High Commissioner for Refugees (UNHCR)"
        ],
        "programming": [],
        "funding": [
            "Fundaci\u00f3n ACNUR Comit\u00e9 Argentino",
            "Private donors",
            "Government of Japan",
            "Australia for UNHCR",
            "Republic of Korea",
            "USA for UNHCR",
            "UN-Habitat",
            "Denmark - Ministry of Foreign Affairs",
            "Government of the United Arab Emirates",
            "European Commission - Humanitarian Aid & Civil Protection",
            "Sweden for UNHCR",
            "Espa\u00f1a con ACNUR",
            "UNO-Fl\u00fcchtlingshilfe",
            "Governmental donors of unearmarked and flexible funds",
            "Government of France",
            "United Nations Central Emergency Response Fund (CERF)",
            "Japan for UNHCR",
            "UK for UNHCR",
            "Sweden, through Swedish International Development Cooperation Agency (Sida)",
            "United States",
            "Germany - Federal Foreign Office"
        ]
    },
    "sectors": {
        "dac": [
            "73010",
            "72010",
            "72050"
        ],
        "humanitarian": [
            "Gender Based Violence",
            "Education",
            "Health",
            "Early Recovery",
            "Emergency Shelter and NFI",
            "Protection"
        ]
    },
    "locations": {
        "countries": [
            "SO"
        ],
        "admin1": [
        ],
        "admin2": [
            "Luuq",
            "Hargeysa",
            "Bossaso",
            "Kismaayo",
            "Garoowe",
            "Gaalkacyo",
            "Berbera"
        ],
        "unclassified": [
            "Mogadishu",
            "Somalia Liaison Support Office",
            "Dhobley",
            "Baidoa"
        ]
    },
    "dates": {
        "start": "2020-01-01",
        "end": "2020-12-31"
    }
}
```

## Author

Started by David Megginson.

## License

This software is in the PUBLIC DOMAIN, and comes with no warranty. See UNLICENSE.md for details.
