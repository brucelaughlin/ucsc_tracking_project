#!/bin/bash

shopt -s nullglob
#shopt -s extglob

# Copied from the "main" scripts on Tsunami


###############################################################################
# Choose the number (0-2) of the projection
###############################################################################
projectionNumber=0
###############################################################################


###############################################################################
# Must change this to avoid overwriting old output
###############################################################################
experimentDir_pre="drift_150_physics_only_AKs_1en5_projections"

###############################################################################



projectionDirectories=("WC15N_GFDLTV" "WC15N_HADTV" "WC15N_IPSLTV")

baseInputDir_pre="/data/blaughli/jerome_projections"
baseInputDir="${baseInputDir_pre}/${projectionDirectories[$projectionNumber]}"

baseOutputDir="/data/blaughli/tracking_project_output_projections"
experimentDir="${experimentDir_pre}_${projectionDirectories[$projectionNumber]}"
outputDir="${baseOutputDir}/${experimentDir}"


echo "InputDir: ${baseInputDir}"
echo "OutputDir: ${outputDir}"

driftDays=150

dtCalc=60
#dtCalc=1440

dtSave=1440

bufferLength=100 # default, but must be provided in my code


idleNodeRegex="([^\/]+$)"

#maxNodes=4
maxNodes=6

nSeed=20

seedSpacing=2

dayNudgeRun=$(( $nSeed*$seedSpacing ))
#echo "$dayNudgeRun"

numRunsPerJob=5
#numRunsPerJob=6
dayNudgeJob=$(( $dayNudgeRun*$numRunsPerJob ))
#echo "$dayNudgeJob"


# "https://stackoverflow.com/questions/52275988/populate-an-array-with-list-of-directories-existing-in-a-given-path-in-bash"
runDirArray=($baseInputDir/Run_*)    # This creates an array of the full paths to all subdirs
#runDirArray=($baseInputDir/Run_*/)    # This creates an array of the full paths to all subdirs

# for testing, only use first year
#runDirArray=("${runDirArray[@]:0:1}")


#printf '%s\n' "${runDirArray[@]}"



declare -a daysPerYearArray
declare -a cumulativeDaysYearArray
#cumulativeDaysYearArray+=0

for ii in "${!runDirArray[@]}" 
do
    runYearArray=(${runDirArray[ii]}/wc15n_avg_*.nc) 
    daysPerYearArray+=(${#runYearArray[@]})
done

printf '%s\n' "${runYearArray[@]}"
#printf '%s\n' "${daysPerYearArray[@]}"

totalDays=0
for ii in ${!daysPerYearArray[@]}
do
    let totalDays+=${daysPerYearArray[ii]}

    sum=0

    for ((jj=0; jj<=$ii; jj++))
    do
        let sum+=${daysPerYearArray[jj]}
    done
    cumulativeDaysYearArray+=($sum)
done

#echo "$totalDays"
#printf '%s\n' "${#cumulativeDaysYearArray[@]}"
#printf '%s\n' "${#daysPerYearArray[@]}"

#numYears=${#daysPerYearArray[@]}

#daysBeforeFinalYear=${cumulativeDaysYearArray[-2]}

#echo "$daysBeforeFinalYear"

