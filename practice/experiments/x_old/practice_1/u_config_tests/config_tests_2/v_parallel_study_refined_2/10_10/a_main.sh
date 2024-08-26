#!/bin/bash

#------------------------------------------------------
# Change nSeed for the other parallel experiments
#------------------------------------------------------
nSeed=10
#--------------------------------

parentDir=$(pwd)

dtCalc=60

dtSave=1440

declare -a startNudgeArray=(
[0]=0
[1]=$(( nSeed*2 ))
[2]=$(( nSeed*4 ))
[3]=$(( nSeed*6 ))
[4]=$(( nSeed*8 ))
[5]=$(( nSeed*10 ))
[6]=$(( nSeed*12 ))
[7]=$(( nSeed*14 ))
[8]=$(( nSeed*16 ))
[9]=$(( nSeed*18 ))
)

bufferLength=100 # default, but must be provided in my code

./a_call_slurm_parallel.sh $dtCalc $dtSave $bufferLength $nSeed "${startNudgeArray[@]}" &

