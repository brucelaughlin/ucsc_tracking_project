#!/bin/bash

dtCalc=60

dtSave=60

declare -a bufferLengthArray=(
[0]=5
[1]=10
[2]=25
[3]=50
[4]=100
[5]=200
)

#bufferLength=100 # default, but must be provided in my code

for ii in ${bufferLengthArray[@]}; do
    ./a_call_slurm_single_allFloats.sh $dtCalc $dtSave $ii &
done
