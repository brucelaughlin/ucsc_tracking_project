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
[1]=$(( nSeed*2 ))
)



bufferLength=100 # default, but must be provided in my code

for ii in ${startNudgeArray[@]}; do
    #./a_call_slurm_varStart.sh $dtCalc $dtSave $bufferLength $nSeed $ii &
    echo $ii
done
