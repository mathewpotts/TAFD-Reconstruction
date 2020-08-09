#!/bin/bash

# Purpose: Send processed data back to tadserv

processed_dir="/home/tamember/matt/tax4md/work"

# Transfer processed data back to tadserv
rsync -Pau ${processed_dir}/calib_db tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/dacset tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/ontime tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/pass0 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/pass2 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/pass3 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/pass4 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/pass5 tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/process tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
rsync -Pau ${processed_dir}/weather tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4_processed/
