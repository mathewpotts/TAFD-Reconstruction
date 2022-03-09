#!/bin/bash
# Designed to work in tandum with Tareq's process scripts this just allows the functionality to choose a date range to process files
# Matt Potts 2022/01/5

#function on how to use script 
print_usage() {
    printf "
Usage: $0 -d <detector> -s <yyyymmdd> -e <yyyymmdd> -p <0-4> -q <0-4>
    [-d : Detector files md,tale,mdtax4,brtax4 (required)]
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
    raw="/home/tamember/$1/raw"
    work="/home/tamember/md/work"
    for dir in $raw/*; do
        if [ $1 == "tale" ] || [ $1 == "mdtax4" ] || [ $1 == "brtax4" ]; then
	    detector_work-flow.sh "$1" "${dir:4:8}" "$end_pass" "$st_pass" 0
        elif [ $1 == "md" ]; then
            mn=$(date -d "${dir##*/}" +'%m')
           yr=$(date -d "${dir##*/}" +'%Y')
           d=$(date -d "${dir##*/}" +'%d')
           md_process.py -i "$dir"/y"$yr"m"$mn"d"$d".md.log -o "$work"/"${dir##*/}" -s "$pass" -3 
        else
            printf "${det} not found.. Please look at the options."
        fi
    done
    exit 0
    }

#Default options
end=$(date +"%Y%m%d")
st_pass=1
end_pass=5

#grab user input
while getopts ":d:s:e:p:q:ha" flag; do
    case $flag in
	d) det="${OPTARG}" ;;
	s) st="${OPTARG}" ;;
	e) end="${OPTARG}" ;;
	p) st_pass="${OPTARG}" ;;
	q) end_pass="${OPTARG}" ;;
	h) print_usage ;;
	a) all_files "$det";;
	:) echo "Option -${OPTARG} requires an argument"; exit 1;
    esac
done

echo
echo '-------------------------------------------------'
echo ' Detector :' ${det}
echo '    Start :' ${st}
echo '      End :' ${end}
echo '-------------------------------------------------'

#process selected range
for dir in $(seq $st $end); do
    f="/home/tamember/data/${det}/raw/${dir}"
    if [ -e $f ] ; then
	echo
        echo '-------------------------------------------------'
	echo "Processing.. ${dir}-${det}"
	echo '-------------------------------------------------'
 	if [ $det == "tale" ] || [ $det == "mdtax4" ] || [ ${det} == "brtax4" ];then
            detector_work-flow.sh "$det" "${dir}" "$end_pass" "$st_pass" 0
	elif [ $det == "md" ];then
            mn=$(date -d "${f##*/}" +'%m')
            yr=$(date -d "${f##*/}" +'%Y')
            d=$(date -d "${f##*/}" +'%d')
            md_process.py -i "$f"/y"$yr"m"$mn"d"$d".md.log -o /home/tamember/mdfd/work/"${f##*/}" -s "$pass" -3
        else
            printf "${det} not found. Please look at the options."
        fi
        echo '-------------------------------------------------'
    fi
done
