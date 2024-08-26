#!/bin/bash

metadata=01_60_60
#metadata: numFloats_dtCalc_dtSave

#SBATCH --job-name $metadata
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu


cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input

opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave.py  &> z_output/log_${metadata}.txt 
