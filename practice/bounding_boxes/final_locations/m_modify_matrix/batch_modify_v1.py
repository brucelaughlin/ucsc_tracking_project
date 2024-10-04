#!/bin/bash

# Call the "modify" script on all settle algorithm aoutput in a directory


#--------------------------------------------------------------------------
# Must specify directory containing output directories to process
#--------------------------------------------------------------------------
baseDir="/home/blaughli/tracking_project/practice/bounding_boxes/final_locations/z_output/z_pre_swap"
#--------------------------------------------------------------------------



dirArray=($baseDir/*.npz)
 
for f_file in "${dirArray[@]}"; do

    python modify_matrix_v11.py "$f_file"
    
done
wait # I don't know why I was using "wait" here.  I think the "&" above is required to make the python calls run in parallel

