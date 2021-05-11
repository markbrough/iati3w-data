Methodology notes
=================

## General

* unless there is an IATI organisation identifier, identify organisations by string matching. There are many variant spellings. The string-matching map is in [inputs/org-map.json](inputs/org-map.json)

* use string matching for locations as well, via [inputs/location-map.json](inputs/location-map.json)

* skip organisations flagged with "skip" in org-map.json

## 3W data

* 3W activities do not have identifiers, so construct pseudo-identifiers by hashing the title, description, organisations, sectors, and locations

* the Somalia 3W data does not include real districts for Banadir Region (Mogadishu), but reporting organisations often write them into the location field. Infer the district from that text when possible.

* when district and region conflict, trust the district and correct the region

* normalise the spelling of humanitarian cluster names using [inputs/humanitarian-cluster-map.json](inputs/humanitarian-cluster-map.json)

* 3W activities will always have a reporting/programming org, and will have a maximum of 1 funder and implementing partner (which may be the same org)

* 3W activities will always have a maximum of 1 region and district

* assume that "MOH" refers to the Somaliland Ministry of Health in the regions that make up Somaliland, and to the Somalia Ministry of Health in other regions.

* the Somalia 3W data only rarely and inconsistently identifies local actors, so ignore that field.

* organisations in the 3W data never have IATI organisation identifiers, so we always identify them via string matching.

* associate the programming organisation with the funder and implementing org (if available), but do not associate the funder and implementing org directly as partners.

* flag all 3W activities as humanitarian

* many 3W activities include demographic information about the people targeted

## IATI data

* all IATI activities and all reporting orgs have persistent, unique identifiers

* roll OECD DAC3 and DAC5 purpose codes up to DAC groups, using [inputs/dac3-sector-map.json](inputs/dac3-sector-map.json)

* map DAC groups to humanitarian clusters when possible, also using [inputs/dac3-sector-map.json](inputs/dac3-sector-map.json)

* IATI activities may be associated with multiple funding orgs, programming orgs, and implementing partners, but always just one reporting org

* IATI activities may be associated with multiple regions and districts

* associate the reporting organisation in IATI data as a partner with each of the participating orgs, and the provider and receiver orgs for transactions

* IATI org type codes are not generally useful for identifying local actors, so rely on [inputs/org-map.json](inputs/org-map.json) instead

* assume an IATI activity is humanitarian if the activity or any of the transactions has the humanitarian marker, if humanitarian-scope is present, and/or if it mentions a humanitarian sector

* all locations use string matching; fill in the admin1 and admin2 from any matches (even if it's just a placename) using [inputs/location-map.json](inputs/location-map.json)

* ignore activities with no sectors
