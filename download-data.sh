#!/bin/bash


THREEW_URL='https://proxy.hxlstandard.org/data/8acb4c.csv'
DPORTAL_SPEC='http://www.d-portal.org/q.xml?from=act,country,dates&country_code=SO&day_end_gteq=2020-01-01&limit=100&offset=%d'

# Make the downloads directory
mkdir -p downloads

# Download the 3W data
wget -v -O downloads/3w-som.csv "$THREEW_URL"
if [ $? -ne 0 ]
then
    1>&2 echo "Failed to download $THREEW_URL"
    exit 1
fi

# Keep downloading 100 IATI activities at a time until we get an empty one
for i in {0..1000000..100}
do
    url=$(printf $DPORTAL_SPEC $i)
    filename=downloads/iati-som-$(printf "%05d" $i).xml
    
    wget -v -O "$filename" "$url"

    # Did the download fail
    if [ $? -ne 0 ]
    then
        1>&2 echo "Failed to download $filename"
        exit 1
    fi
    if ! $(grep -q "<iati-activity" "$filename")
    then
        rm "$filename"
        break
    fi
done

exit 0

