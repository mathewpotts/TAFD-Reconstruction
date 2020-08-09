#!/usr/bin/env bash
# Designed to work in tandum with Tareq's process scripts this just allows the functionality to choose a date range to process files
# Matt Potts 2019/01/08

#function on how to use script 
print_usage() {
    printf "Usage: $0 \n [-s : Start date <yyyymmdd>] \n [-e : End date range <yyyymmdd>. (Defaults to Current Date)] \n [-p : What Pass to stop at <1-13>. (Defaults to 13)] \n [-a : Process all files in data directory. If you need to process all files only to a certain pass then place the -p flag before -a. (./process.sh -p 4 -a)] \n"
    exit
    }
if (($# == 0))
then
    print_usage
    exit 1
fi
#function to process all data in raw file
all_files() {
    for dir in raw/*; do
	mn=$(date -d "${dir##*/}" +'%m')
	yr=$(date -d "${dir##*/}" +'%Y')
	d=$(date -d "${dir##*/}" +'%d')
	md_process.py -i "$dir"/y"$yr"m"$mn"d"$d".md.log -o work/"${dir##*/}" -s "$pass" -3
    done
    exit 0;
    }

#Default options
pass=13
end=$(date +"%Y%m%d")

#grab user input
while getopts ":s:e:p:ha" flag; do
    case $flag in
	s) st="${OPTARG}" ;;
	e) end="${OPTARG}" ;;
	p) pass="${OPTARG}" ;;
	h) print_usage ;;
	a) all_files ;;
	:) echo "Option -${OPTARG} requires an argument"; exit 1;
    esac
done

#process selected range
for dir in $(seq $st $end); do
    f="raw/${dir}"
    if [ -e $f ]; then
	mn=$(date -d "${f##*/}" +'%m')
	yr=$(date -d "${f##*/}" +'%Y')
	d=$(date -d "${f##*/}" +'%d')
	md_process.py -i "$f"/y"$yr"m"$mn"d"$d".md.log -o work/"${f##*/}" -s "$pass" -3
	echo
    fi
done
