#!/bin/bash

numFloats=82

#dtCalc=15
dtCalc=60

#declare -a dtCalcArray=(
#[0]=1
#)
declare -a dtCalcArray=(
[0]=1
[1]=5
[2]=10
[3]=15
[4]=30
[5]=60
)

dtSave=60
#declare -a dtSaveArray=(
#[0]=1
#[1]=5
#[2]=10
#[3]=15
#[4]=30
#[5]=60
#)

bufferLength=100 # default, but must be provided in my code

#for ((dtCalc=; numFloats <= $max_numFloats; numFloats=${numFloats}*10)); do
for ii in ${dtCalcArray[@]}; do
    ./a_call_slurm_single.sh $numFloats $ii $dtSave $bufferLength &
done
