#!/bin/bash

#SBATCH --job-name 01_01_01
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd /home/blaughli/tracking_project/practice/experiments/practice_1/sanity_check

python opendrift_run_store_eco_variables_1_of_1.py &> z_output/log_1.txt 
