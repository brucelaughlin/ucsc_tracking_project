#!/bin/bash

logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})"

#SBATCH --job-name ${logString}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu


#cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/config_tests_2/separation_study_v2

cd $parentDir

#python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240321_sepTest.py $dtCalc $dtSave $bufferLength &> z_output/log_${logString}.txt 
python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240321_sepTest.py $dtCalc $dtSave $bufferLength $parentDir &> z_output/log_${logString}.txt 

