#!/bin/bash

#SBATCH --job-name 03_02_06
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=36G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/release_runs_lastRelease_03_02_06

python opendrift_run_store_eco_variables_1_of_2.py &> z_output/log_1.txt &
python opendrift_run_store_eco_variables_2_of_2.py &> z_output/log_2.txt
