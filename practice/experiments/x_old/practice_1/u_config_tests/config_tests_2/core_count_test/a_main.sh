#!/bin/bash

#------------------------------------------------------
# Change nSeed to 40 for the other parallel experiment
#------------------------------------------------------
nSeed=20
#--------------------------------

parentDir=$(pwd)

dtCalc=60

dtSave=1440

declare -a startNudgeArray=(
[0]=0
)

bufferLength=100 # default, but must be provided in my code

./a_call_slurm_parallel.sh $dtCalc $dtSave $bufferLength $nSeed "${startNudgeArray[@]}" &


#echo ${startNudgeArray[0]}





