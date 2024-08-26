#!/bin/bash

#parentDir='/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/config_tests_2/separation_study_v2/'

parentDir=$(pwd)

cd $parentDir # seems unnecessary

dtCalc=30

declare -a dtSaveArray=(
[0]=30
[1]=60
[2]=120
[3]=240
[4]=480
[5]=720
[6]=1440
)


bufferLength=100 # default, but must be provided in my code

for ii in ${dtSaveArray[@]}; do
    ./a_call_slurm_varInputFile.sh $dtCalc $ii $bufferLength $parentDir &
done
