#!/bin/bash
sort -k 3 -k 2n -t ',' -o ./data_processing/output.csv ./data_processing/file_url_counts.csv
awk -F',' '{print $1}' ./data_processing/output.csv |sort|uniq -d|grep -F -f - ./data_processing/output.csv | sort -k1 -t ',' ./data_processing/multiple_repos.csv