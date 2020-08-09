#!/bin/bash
# Designed to work in tandum with Tareq's process scripts this just allows the functionality to choose a date range to process files
# Matt Potts 2020/01/28

#function on how to use script 
print_usage() {
    printf "
Usage: $0 -s <yyyymmdd> -e <yyyymmdd> -p <0-4> -q <0-4>
    [-s : Start date <yyyymmdd>]
    [-e : End date range <yyyymmdd>. (Defaults to Current Date)]
    [-p : What Pass to start at <0-5>. (Defaults to 1)]
    [-q : What Pss to end at <1-5>, (Defaults to 5)] 
    [-a : Process all files in data directory. If you need to process all files only to a certain pass then place the -p flag before -a. (./process_mdtax4.sh -p 4 -a)]
    
Pass # defined as follows: (out of date...)
    [0 : run pass0 script (tlfdp0 program: produces dst files from raw data)]
    [1 : calculate weather codes]
    [2 : calculate dac settings]
    [3 : calculate detector ontime]
    [4 : calculate tube gains]
"
    exit
    }
if (($# == 0)); then
    print_usage
    exit 1
fi

#function to process all data in raw dir
all_files() {
    for dir in raw/*; do
	detector_work-flow.sh tale "${dir:4:8}" "$end_pass" "$st_pass" 0
    done
    exit 0
    }

#Default options
end=$(date +"%Y%m%d")
st_pass=1
end_pass=5

#grab user input
while getopts ":s:e:p:q:ha" flag; do
    case $flag in
	s) st="${OPTARG}" ;;
	e) end="${OPTARG}" ;;
	p) st_pass="${OPTARG}" ;;
	q) end_pass="${OPTARG}" ;;
	h) print_usage ;;
	a) all_files ;;
	:) echo "Option -${OPTARG} requires an argument"; exit 1;
    esac
done

#process selected range
for dir in $(seq $st $end); do
    f="/home/tamember/matt/tale/raw/${dir}-tale"
    if [ -e $f ] ; then
	echo "Processing.. ${dir}-tale"
	echo
	detector_work-flow.sh tale "${dir}" "$end_pass" "$st_pass" 0
    fi
done
