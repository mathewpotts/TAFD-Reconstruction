#!/usr/bin/env bash
# Purpose: Automatically transfer MD data to tale00 pc from tadserv, process it using UTAFD, transfer it to tadserv, and clean up directories every month.
# Author: Mathew Potts
# Updated: 6/25/2020

source /home/tamember/.bashrc
source /home/tamember/root/bin/thisroot.sh
source /home/tamember/with-cuda.sh

# Defining variables
d=$(date +%d)
main_dir="/home/tamember/matt/md"
data_dir="/home/tamember/matt/md/raw/"
processed_dir="/home/tamember/matt/md/work/"

# Cleaning up directories at the beginning of every month
if [ ${d} == "01" ]; then
        rm -rf ${data_dir}/*
        rm -rf ${processed_dir}/*
	rm -rf ${main_dir}/process_logs/*
fi

# Transfer all data from tadserv mdfd data directory to proper work directory and wait till tranfer is done
rsync -Pau --exclude="MD5SUMS" tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdfd/ ${data_dir}/

wait

#Set start and end of processing range
START=$(ls ${data_dir} | sort -n | head -n 1)
END=$(ls ${data_dir} | sort -n | tail -n 1)

# Process a sequence of data using Tareqs process script and transfer processed data to tadserv
for dir in $(seq $START $END); do
    f="${data_dir}/$dir"
    g="${processed_dir}/$dir"
    if [ -d $f ] && [ ! -d $g ]; then
	echo "Starting md_process.py..."
	mn=$(date -d "${f##*/}" +'%m')
	yr=$(date -d "${f##*/}" +'%Y')
	d=$(date -d "${f##*/}" +'%d')
	/home/tamember/software/TA/UTAFD/build/with-cuda/release/bin/md_process.py -i ${f}/y${yr}m${mn}d${d}.md.log -o $processed_dir/${f##*/} -3
	echo

	# Transfer processed data back to tadserv
	rsync -Pau ${processed_dir}/${f##*/} tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdfd_processed/mdfd${yr:2:2}.ps5/
    fi
done
