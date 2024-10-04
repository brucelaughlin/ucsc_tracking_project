#!/bin/bash

# Call the "modify" script on all settle algorithm aoutput in a directory


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
# Must specify directory containing output directories to process
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
baseDir="/home/blaughli/tracking_project/practice/bounding_boxes/final_locations/z_output/z_pre_swap/z_swapped"
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------



dirArray=($baseDir/*.npz)
   
#tA=(0)

for f_file in "${dirArray[@]}"; do

    #echo "$settleFile"
    python plot_con_seasonal_v4.py "$f_file"

done
wait # I don't know why I was using "wait" here.  I think the "&" above is required to make the python calls run in parallel

