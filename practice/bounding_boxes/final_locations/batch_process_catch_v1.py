#!/bin/bash

# Call the catch script on all tracking runs in a directory


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
# Must specify directory containing run output directories to process
#--------------------------------------------------------------------------
# MUST CHANGE "baseYear" DEPENDING ON THE BASE YEAR OF THE TRACKING RUN
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#runBaseDir="/data/blaughli/copiedFiles/y_projections_1990_2020_KEEP/y_complete"
#baseYear=1990
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
runBaseDir="/data/blaughli/copiedFiles/y_projections_1990_2020_KEEP/y_complete_1988"
baseYear=1988
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------



#callingDir="$(pwd)"
runDirArray=($runBaseDir/*)
   
#tA=(0)

#for runDir in "${runDirArray[@]}"; do
#for ii in "${!tA[@]}"; do
for ii in "${!runDirArray[@]}"; do

    screen -dmS "run_$ii" python catch_settled_points_v19.py --trackingdir ${runDirArray[$ii]} --baseyear $baseYear
    #screen -dmS "run_$ii" python catch_settled_points_v18.py --trackingdir $runDirArray[$ii] --baseyear $baseYear &
    #python catch_settled_points_v18.py --trackingdir $runDir --baseyear $baseYear &
    

done
wait # I don't know why I was using "wait" here.  I think the "&" above is required to make the python calls run in parallel

