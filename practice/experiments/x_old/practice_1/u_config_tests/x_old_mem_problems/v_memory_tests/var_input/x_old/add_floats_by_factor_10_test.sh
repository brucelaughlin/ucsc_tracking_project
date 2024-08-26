#!/bin/bash

#max_num_floats=11839

start_num=10000
max_num_floats=99999

dtCalc=60

dtSave=60

#for ((num_floats=1; num_floats <= $max_num_floats; num_floats=${num_floats}*10)); do
for ((num_floats=$start_num; num_floats <= $max_num_floats; num_floats=${num_floats}*10)); do
   ./call_slurm_single.sh $num_floats $dtCalc $dtSave &
done
