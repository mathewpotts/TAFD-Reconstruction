#!/bin/bash

# Purpose: Transfer files from tadserv to local data dir

rsync -Pau tamember@tadserv.physics.utah.edu:/pool02/tadserv5/tafd/mdtax4/ ~/matt/tax4md/raw/
