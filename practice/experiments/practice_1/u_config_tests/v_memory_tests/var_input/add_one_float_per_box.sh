#!/bin/bash

#max_num_floats=82
max_num_floats=4

dtCalc=60

dtSave=60

for ((num_floats=1; num_floats <= $max_num_floats; num_floats+=1)); do
   ./call_slurm_single.sh $num_floats $dtCalc $dtSave & 
done
