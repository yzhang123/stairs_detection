#!/bin/bash

######
# usage:
# url_root: path to directory where all url folders are stored, e.g. git_root/urls
# key_word: search key, e.g. stairs
# n_pages: the first number of pages of flickr that are scraped
# outFile: specify the path to file where all url are stored

######
url_root=$1 #$HOME/code/stairs_detection/urls
key_word=$2 # e.g. steps
n_pages=$3 # number of search pages
outFile=$4

if [ ! -d "$url_root" ]; then
    echo "making dir $url_root"
        mkdir -p $url_root
fi

out_dir="$url_root/$key_word"

if [ ! -d "$out_dir" ]; then
    echo "making dir $out_dir"
        mkdir -p $out_dir
fi 



echo "outFile: $outFile"
if [ -f "$outFile" ]; then
    echo "delete existing output File"
    rm $outFile
fi

for i in `seq -f "%03g" 1 $n_pages`; do
    temp_file="$out_dir/tmp$i"
    echo "temp file $temp_file"
    #outputFile="$out_dir/page$i"
    curl -o $temp_file "https://www.flickr.com/search/?text=$key_word&page=$i"
    grep modelExport $temp_file \
    | sed -e 's@\\@@g'| sed -e 's@displayUrl@\n@g'\
    | awk /farm.*\.jpg/ | awk -F "\":\"\/\/" '{print $2}' \
    | awk -F "," '{print $1 " " $2 " " $3}' \
    | sed -e 's@"@@g' >> $outFile
    rm $temp_file
done
