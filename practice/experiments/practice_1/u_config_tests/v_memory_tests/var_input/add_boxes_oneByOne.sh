#!/bin/bash

#max_num_floats=11839

max_num_floats=200



#num_floats_incrememnt=150
    
for ((num_floats=1; num_floats < $max_num_floats; num_floats+=150)); do
    
    num_floats=$((num_floats+num_floats_increment))
    #echo $num_floats

   ./call_slurm_single.sh $num_floats & 

done







#num_floats=1

# Why don't these work????

#while [[ $num_floats -le $max_num_floats ]]
#do
#for ((num_floats=1; num_floats < $max_num_floats; num_floats+=${num_floats_increment})); do
#for ((num_floats=1; $num_floats < $max_num_floats; num_floats+=${num_floats_increment})); do
#for ((num_floats=1; $num_floats < $max_num_floats; num_floats+=150)); do
#for ((num_floats=1; $num_floats < $max_num_floats; num_floats+=$num_floats_increment)); do
#do
    #num_floats=$(($num_floats + $num_floats_increment))
    #num_floats+=${num_floats_increment}
