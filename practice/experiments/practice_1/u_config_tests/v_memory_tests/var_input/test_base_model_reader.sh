#!/bin/bash

num_floats=1000000

#dtCalc=15
dtCalc=60

dtSave=60
#dtSave=1440

bufferLength=100 # default, but must be provided in my code
#bufferLength=50
#bufferLength=10

./call_slurm_single.sh $num_floats $dtCalc $dtSave $bufferLength &
