#!/bin/bash

#------------------------------------------------------
# Change nSeed for the other parallel experiments
#------------------------------------------------------
nSeed=1
#--------------------------------

parentDir=$(pwd)

dtCalc=1440

dtSave=1440

declare -a startNudgeArray=(
[0]=0
)

bufferLength=100 # default, but must be provided in my code

./a_call_slurm_parallel.sh $dtCalc $dtSave $bufferLength $nSeed "${startNudgeArray[@]}" &

