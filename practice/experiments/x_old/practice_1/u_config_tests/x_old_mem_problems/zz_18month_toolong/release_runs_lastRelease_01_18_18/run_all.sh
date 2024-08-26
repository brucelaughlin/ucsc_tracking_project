#!/bin/bash

#SBATCH --job-name 18_01_18
#SBATCH --ntasks=1

#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/release_runs_lastRelease_18_01_18

python opendrift_run_store_eco_variables_1_of_1.py &> z_output/log_1_err.txt &
