#!/bin/bash

#parentDir='/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/config_tests_2/separation_study_v2/'

parentDir=$(pwd)

dtCalc=60

dtSave=1440

declare -a nSeedArray=(
[0]=60
)


bufferLength=100 # default, but must be provided in my code

for ii in ${nSeedArray[@]}; do
    ./a_call_slurm_varInputFile_varSeed_printRunDay.sh $dtCalc $dtSave $bufferLength $ii &
done
