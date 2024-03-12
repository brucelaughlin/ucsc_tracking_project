#!/bin/bash

#logString="$(printf %05d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})"
logString="$(printf %05d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})_$(printf %03d ${bufferLength})"

#SBATCH --job-name ${logString}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu


cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/opendrift_stock_tests

#python example_generic.py $numFloats &> z_output/log_${logString}.txt 
python example_generic.py $numFloats $dtCalc $dtSave $bufferLength &> z_output/log_${logString}.txt 
