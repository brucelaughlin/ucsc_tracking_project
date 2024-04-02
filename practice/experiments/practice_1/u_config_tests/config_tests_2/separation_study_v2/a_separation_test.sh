#!/bin/bash

declare -a dtCalcArray=(
[0]=1
[1]=5
[2]=10
[3]=15
[4]=30
[5]=60
)

#declare -a dtCalcArray=(
#[0]=60
#)

dtSave=60

bufferLength=100 # default, but must be provided in my code

for ii in ${dtCalcArray[@]}; do
    ./a_call_slurm_varInputFile.sh $ii $dtSave $bufferLength &
done
