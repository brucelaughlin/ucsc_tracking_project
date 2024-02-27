#!/bin/bash

#SBATCH --job-name 01_60_2880
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/num_floats_write_dt_min_compute_dt_min_01_60_2880

python opendrift_run_store_eco_variables_spec_numfloats_dt.py &> z_output/log_1.txt 
