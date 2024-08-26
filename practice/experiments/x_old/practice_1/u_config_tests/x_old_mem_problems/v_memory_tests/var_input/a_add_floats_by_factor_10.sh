#!/bin/bash

#max_num_floats=11839
#max_num_floats=10000
num_floats=1000000

#dtCalc=15
dtCalc=60

dtSave=60
#dtSave=1440

bufferLength=100 # default, but must be provided in my code
#bufferLength=50
#bufferLength=10

#for ((num_floats=1; num_floats <= $max_num_floats; num_floats=${num_floats}*10)); do
#for ((num_floats=10000; num_floats <= $max_num_floats; num_floats=${num_floats}*10)); do
   #./call_slurm_single.sh $num_floats $dtCalc $dtSave &
   #./call_slurm_single.sh $num_floats $dtCalc $dtSave $bufferLength &
./call_slurm_single.sh $num_floats $dtCalc $dtSave $bufferLength &
#done
