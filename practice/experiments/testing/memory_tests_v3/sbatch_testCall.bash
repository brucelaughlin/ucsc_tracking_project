#!/bin/bash

#SBATCH --job-name opendrift
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu


python opendrift_run_store_eco_variables_240830_memTest_configFile_v1.py --configfile $configFile --jobrunnumber $jobRunNum



#python opendrift_run_store_eco_variables_240830_memTest_configFile_v1.py --configfile $configFile --jobrunnumber $jobRunNum &> $logFile &
#python opendrift_run_store_eco_variables_240830_memTest_configFile_v1.py --configfile config.yaml --jobrunnumber 0 &> z_testLog.txt &

