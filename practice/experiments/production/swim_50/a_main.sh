#!/bin/bash

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
experimentDir="drift_150_swim_speed_50"
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

maxNodes=8
#maxNodes=4
#maxNodes=6

nSeed=20

seedSpacing=2

dayNudgeRun=$(( $nSeed*$seedSpacing ))
#echo "$dayNudgeRun"

numRunsPerJob=6
dayNudgeJob=$(( $dayNudgeRun*$numRunsPerJob ))
#echo "$dayNudgeJob"


#baseInputDir="/data03/fiechter/WC15N_1988-2010/"
baseInputDir="/data03/fiechter/WC15N_1988-2010"

# "https://stackoverflow.com/questions/52275988/populate-an-array-with-list-of-directories-existing-in-a-given-path-in-bash"
runDirArray=($baseInputDir/Run_*/)    # This creates an array of the full paths to all subdirs
#runDirArray=("${runDirArray[@]%/}")    # This removes the trailing slash on each item

# for testing, only use first year
#runDirArray=("${runDirArray[@]:0:1}")


#printf '%s\n' "${runDirArray[@]}"



declare -a daysPerYearArray
declare -a cumulativeDaysYearArray
#cumulativeDaysYearArray+=0

for ii in "${!runDirArray[@]}" 
do
    #runYearArray=(${runDirArray[ii]}/wc15n_avg_*.nc) 
    runYearArray=(${runDirArray[ii]}wc15n_avg_*.nc) 
    daysPerYearArray+=(${#runYearArray[@]})
done

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
daysBeforeFinalYear=${cumulativeDaysYearArray[-2]}
#echo "$daysBeforeFinalYear"


lastSeedDay=$(( totalDays-driftDays ))
#lastSeedDay=$(( totalDays-90 ))

# Make array of days cumulative days seeded, or seeding start days (nudge, not exact date), and then iterate through,
# using the cumulativeDaysYearArray to check if need to switch yearNudge passed to script (so we always only ever load a max of 
# 2 years with readers).  When in final year, set the flag, don't load next year.  Also can just make a seeding array that
# stops <driftDays> days before last day of last year, to control seeding.  Test this all with script printing relavant output,
# ... or perhaps slurm jobs seeding a single particle so they're fast...



numRuns=$(( (totalDays + (dayNudgeRun-1))/dayNudgeRun ))
#echo "$numRuns"
numJobs=$(( (totalDays + (dayNudgeJob-1))/dayNudgeJob ))
#echo "$numJobs"


dayNudge=0
#dayNudge=8034


runYear=0

#nodesIdle=0

for (( ii = 0 ; ii <= numJobs ; ii ++  )); 
#for (( ii = 0 ; ii <= 8 ; ii ++  )); 
#for (( ii = 0 ; ii < 1 ; ii ++  )); 
do

    #if  (( $(squeue -u blaughli -h -t running | wc -l) <= $maxNodes )); then
    #    echo "$(squeue -u blaughli -h -t running | wc -l)"
    #fi

    # Only submit new job if we aren't using our allowed number of nodes 
    #while [ $(squeue -u blaughli -h -t running | wc -l) -ge $maxNodes ]; do 
    while (( $(squeue -u blaughli -h -t running | wc -l) >= $maxNodes )); do 
        #sleep 20
        sleep 10
        #echo "$(squeue -u blaughli -h -t running | wc -l)"
    done

    # Only begin attempting anything if there are idle nodes available
    #idleNodeSwitch=1 # TESTING
    idleNodeSwitch=0 
    #while [ idleNodeSwitch == 0  ]; do
    #while [ $idleNodeSwitch == 0  ]; do
    while (( $idleNodeSwitch == 0  )); do
        #sleep 20
        sleep 10
        # Determine the number of idle nodes
        nodeInfoString=$(sinfo -o %A | sed -n '2p')
        [[ $nodeInfoString =~ $idleNodeRegex ]]
        nodesIdle=${BASH_REMATCH[1]}
   

        #if (( nodesIdle > 0  )); then idleNodeSwitch=1; fi
        if (( $nodesIdle > 0  )); then 
            idleNodeSwitch=1; 
        fi
        #if (( nodesIdle <1  )); then idleNodeSwitch=1; fi # JUST FOR TESTING

    done


    dayNudge=$(( ii*dayNudgeJob ))

    if (( $dayNudge > ${cumulativeDaysYearArray[runYear]} ));
    then
        runYear=$((runYear+1))
    fi

    #echo "$runYear"

    readerDir1=${runDirArray[$runYear]}
    
    # Don't add reader for next year if in final year
    if (( $dayNudge+2 > $daysBeforeFinalYear  )); 
    then
        readerDir2=$readerDir1
    else
        readerDir2=${runDirArray[$((runYear + 1))]}
    fi

    #echo "$readerDir1"
    #echo "$readerDir2"
    #echo

    unset startNudgeArray
    declare -a startNudgeArray
    for (( jj = 0; jj < $numRunsPerJob; jj ++))
    do
        currentNudge=$((dayNudge + dayNudgeRun*jj))
        if (( ($currentNudge + $dayNudgeRun - $seedSpacing) > $lastSeedDay  )); then
            break
        fi
        startNudgeArray+=($currentNudge)
    done

    #printf '%s\n' "${startNudgeArray[@]}"
    #echo

    if ((${#startNudgeArray[@]} > 0 )); then
        ./a_call_slurm.sh $dtCalc $dtSave $bufferLength $nSeed $readerDir1 $readerDir2 $outputDir "${startNudgeArray[@]}" &
    fi

    # I think I need to add a sleep call here, to make sure my script catches new runs and doesn't
    # create too many slurm jobs
    sleep 10

done








