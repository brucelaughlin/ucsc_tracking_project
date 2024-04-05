#!/bin/bash

#parentDir='/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/config_tests_2/separation_study_v2/'

parentDir=$(pwd)

cd $parentDir # seems unnecessary

#dtCalc=15
dtCalc=15

#dtSave=15
dtSave=15

declare -a bufferLengthArray=(
[0]=1000
[1]=5000
[2]=10000
[3]=50000
[4]=100000
)
#declare -a bufferLengthArray=(
#[0]=10
#[1]=20
#[2]=40
#[3]=60
#[4]=100
#[5]=200
#[6]=400
#[7]=800
#)


#bufferLength=100 # default, but must be provided in my code

for ii in ${bufferLengthArray[@]}; do
    ./a_call_slurm_varInputFile.sh $dtCalc $dtSave $ii $parentDir &
done
