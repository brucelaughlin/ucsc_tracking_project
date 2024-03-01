#!/bin/bash

#max_num_floats=11839
max_num_floats=10000

dtCalc=15

dtSave=60

for ((num_floats=1; num_floats <= $max_num_floats; num_floats=${num_floats}*10)); do
   ./call_slurm_single.sh $num_floats $dtCalc $dtSave &
done
