#!/usr/bin/env bash
# Purpose: Automatically transfer MD data to tale00 pc from tadserv, process it using UTAFD, transfer it to tadserv, and clean up directories every month.
# Author: Mathew Potts
# Updated: 2/3/2020

source /home/tamember/.bashrc
source /home/tamember/root/bin/thisroot.sh
source /home/tamember/with-cuda.sh

# Defining variables
yr=$(date +%Y)
mn=$(date +%m)
d=$(date +%d)
yyyymmdd=$(date +%Y%m%d)
main_dir="/home/tamember/matt/tax4md"
data_dir="/home/tamember/matt/tax4md/raw/"
processed_dir="/home/tamember/matt/tax4md/work/"

# Cleaning up directories at the beginning of every month
if [ ${d} == "01" ]; then
        rm -rf ${data_dir}/*
        #rm -rf ${processed_dir}/*
	rm -rf ${main_dir}/process_logs/*
fi

# Transfer the data from tadserv to proper work directory and wait till tranfer is done
rsync -Pau tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4/${yyyymmdd}-tax4 ${data_dir}/

wait 

# Process data using process script (output to file) and wait till done
echo "Starting detector_work-flow.sh..."
/home/tamember/software/TA/UTAFD/build/with-cuda/release/process/scripts/detector_work-flow.sh mdtax4 $yyyymmdd 5 1 0

wait

#/home/tamember/software/TA/UTAFD/build/with-cuda/release/process/scripts/detector_run_recon.sh mdtax4 $yyyymmdd

wait

# Transfer processed data back to tadserv
rsync -Pau ${processed_dir}/calib_db tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/dacset tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/ontime tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/pass0 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
#rsync -Pau ${processed_dir}/pass2 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
#rsync -Pau ${processed_dir}/pass3 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
#rsync -Pau ${processed_dir}/pass4 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
#rsync -Pau ${processed_dir}/pass5 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/process tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/weather tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
