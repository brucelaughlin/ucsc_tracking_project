#!/bin/bash

#SBATCH --job-name 04_01_04
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/vv_simpler/releaseDays_runs_lastReleaseDay_04_01_04

python opendrift_run_store_eco_variables_1_of_1.py &> z_output/log_1.txt 
