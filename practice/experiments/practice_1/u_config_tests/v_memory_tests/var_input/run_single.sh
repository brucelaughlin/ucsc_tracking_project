#!/bin/bash

logString="$(printf %05d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})"

#SBATCH --job-name ${logString}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu


cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input

python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_limitFloats.py $numFloats $dtCalc $dtSave  &> z_output/log_${logString}.txt 
#python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_onePerBox.py $numFloats $dtCalc $dtSave  &> z_output/log_${logString}.txt 
