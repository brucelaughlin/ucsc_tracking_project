#!/bin/bash

###############################################################################
###############################################################################
# Testing swimming - so just do 1 year, and ideally even less...  Few particles... just want to see them hug the coasts
###############################################################################
###############################################################################

# Need to modify opendrift caller python script: last run 90 days before end of last year

# Should pass year to script, so script initiates reader for entire year and entire next year.
# And if in final year, don't try to load next year

# Use Jerome's files to send Year and Day to the opendrift caller; within the caller,
# maike the datetime starting date

# Don't worry about "final year flag" ... handle checking for final year in python controller script,
# only load subsequent year reader if not in final year


# Create output and log directory if they don't exist

# Must change this to avoid overwriting old output
###############################################################################
experimentDir="drift_150_swim_test_v2_zeroVel_grad"
###############################################################################

driftDays=150

dtCalc=60
#dtCalc=1440

dtSave=1440

bufferLength=100 # default, but must be provided in my code


baseOutputDir="/data01/blaughli/tracking_project_output"
#baseOutputDir="/data03/blaughli/tracking_project_output"
outputDir=($baseOutputDir/$experimentDir)

#outputDir=$(pwd)/z_output

echo "$outputDir"

# Why can't I "mkdir" now???
####mkdir -p $(pwd)/z_output/z_logs
#mkdir -p $(outputDir)/z_logs

idleNodeRegex="([^\/]+$)"

#maxNodes=4
maxNodes=6

nSeed=1
#nSeed=20

seedSpacing=2



baseInputDir="/home/blaughli/tracking_project/practice/onshore_swim_work/z_dummy_model_input/"
#baseInputDir="/home/blaughli/tracking_project/practice/onshore_swim_work/z_dummy_model_input"
#baseInputDir="/data03/fiechter/WC15N_1988-2010"

readerDir1=$baseInputDir
readerDir2=$baseInputDir

echo "$readerDir1"

echo "hi1"

./a_call_slurm_test_v1.sh $dtCalc $dtSave $bufferLength $nSeed $readerDir1 $readerDir2 $outputDir &


echo "hiEnd1"




