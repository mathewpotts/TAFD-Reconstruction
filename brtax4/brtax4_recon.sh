#!/bin/bash
# Designed to work in tandum with Tareq's process scripts this just allows the functionality to choose a date range to process files
# Matt Potts 2020/07/24

#function on how to use script 
print_usage() {
    printf "
Purpose: Process all pass0 files all the way to pass 5.

Usage: $0 -s <yyyymmdd> -e <yyyymmdd> -p <0-4> -q <0-4>
    [-s : Start date <yyyymmdd>]
    [-e : End date range <yyyymmdd>. (Defaults to Current Date)]
    [-p : What Pass to start at <1-4>. (Defaults to 1)]
    [-q : What Pass to end at <1-4>, (Defaults to 4)] 
    [-a : Process all files in data directory. If you need to process all files only to a certain pass then place the -p flag before -a. (./$0 -p 4 -a)]
    
Pass # defined as follows:
    [1 : run stpln_main (Fits events to the Shower Development Plane (SDP))]
    [2 : run stps2_main (Rayleigh Filter)]
    [3 : run stgeo_main (Fits events to shower geometry)]
    [4 : run stpfl12_main (Fits events shower development profile to reconstructed energy)]
"
    exit
    }
if (($# == 0)); then
    print_usage
    exit 1
fi

#function to process all data in raw dir
all_files() {
    for dir in work/pass0/data/*; do
	detector_run_recon.sh brtax4 "${dir:16:8}" "$end_pass" "$st_pass"
    done
    exit 0
}


#Default options
end=$(date +"%Y%m%d")
st_pass=1
end_pass=4

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
    f="/home/tamember/matt/tax4br/work/pass0/data/${dir}*"
    if [ -e $f ]; then
	detector_run_recon.sh brtax4 "$dir" "$end_pass" "$st_pass"
    fi
done
