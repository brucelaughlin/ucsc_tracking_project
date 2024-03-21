#!/bin/bash

#SBATCH --job-name 01_06_06
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/releaseDays_runs_lastReleaseDay_01_06_06

python opendrift_run_store_eco_variables_1_of_6.py &> z_output/log_1.txt &
python opendrift_run_store_eco_variables_2_of_6.py &> z_output/log_2.txt &
python opendrift_run_store_eco_variables_3_of_6.py &> z_output/log_3.txt &
python opendrift_run_store_eco_variables_4_of_6.py &> z_output/log_4.txt &
python opendrift_run_store_eco_variables_5_of_6.py &> z_output/log_5.txt &
python opendrift_run_store_eco_variables_6_of_6.py &> z_output/log_6.txt
