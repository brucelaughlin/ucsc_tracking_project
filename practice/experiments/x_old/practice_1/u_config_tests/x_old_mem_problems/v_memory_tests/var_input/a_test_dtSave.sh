#!/bin/bash

dtCalc=60

#dtSave=60
declare -a dtSaveArray=(
[0]=60
[1]=120
[2]=240
[3]=480
[4]=960
[5]=1920
)

bufferLength=100 # default, but must be provided in my code

for ii in ${dtSaveArray[@]}; do
    ./a_call_slurm_single_allFloats.sh $dtCalc $ii $bufferLength &
done
