#!/bin/bash

url_dir=scrapes
if [ ! -d "url_dir" ]; then
    echo "making dir $url_dir"
    mkdir -p $url_dir
fi

for i in `seq -f "%03g" 1 500`; do
    temp_file="$url_dir/tmp$i"
    outputFile="$url_dir/page$i"
    curl -o $temp_file "https://www.flickr.com/search/?text=steps&page=$i"
    echo "outputFile" $outputFile
    grep modelExport $temp_file | sed -e 's@\\@@g'| sed -e 's@displayUrl@\n@g'| awk /farm.*\.jpg/ | awk -F "\":\"\/\/" '{print $2}' | awk -F "," '{print $1 " " $2 " " $3}' |sed -e 's@"@@g' > $outputFile
    rm $temp_file
done

