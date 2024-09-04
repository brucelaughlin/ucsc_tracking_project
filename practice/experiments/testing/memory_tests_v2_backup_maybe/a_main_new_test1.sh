#!/bin/bash

# new1: don't worry about specific his files being passed.  keep track with cumulative day dex...

# allow environment variables to be passed after the called script on the command line (see call to call_slurm... at end)
#set -k

# Copied from the "main" scripts on Tsunami


###############################################################################
# Choose the number (0-2) of the projection
###############################################################################

#projectionNumber=0
#projectionNumber=1
#projectionNumber=2

###############################################################################


###############################################################################
# Must change this to avoid overwriting old output
###############################################################################
#experimentDir_pre="drift_150_physics_only_AKs_1en5_projections"
experimentDir_pre="memory_test"
###############################################################################



projectionDirectories=("WC15N_GFDLTV")
#projectionDirectories=("WC15N_GFDLTV" "WC15N_HADTV" "WC15N_IPSLTV")

baseInputDir_pre="/data/blaughli/jerome_projections"
#baseInputDir="${baseInputDir_pre}/${projectionDirectories[$projectionNumber]}"

baseOutputDir="/data/blaughli/tracking_project_output_projections/memory_tests"
#baseOutputDir="/data/blaughli/tracking_project_output_projections"


#experimentDir="${experimentDir_pre}_${projectionDirectories[$projectionNumber]}"
#outputDir="${baseOutputDir}/${experimentDir}"


#echo "InputDir: ${baseInputDir}"
#echo "OutputDir: ${outputDir}"

driftDays=150

dtCalc=60
#dtCalc=1440

dtSave=1440

bufferLength=100 # default, but must be provided in my code

#maxNodes=1
#maxNodes=4
#maxNodes=6
maxNodes=12
	
seedSpacing=2


idleNodeRegex="([^\/]+$)"

                

#printf '%s\n' "${hisFileArray[@]}"

numRunsPerJobArray=(10)
#numRunsPerJobArray=(15 20 25 30 35 40)
#declare -a numRunsPerJobArray=(15 20 25 30 35 40)
#declare -a numRunsPerJobArray=(4 5 6 7 8 9 10)
nSeedArray=(40)
#declare -a nSeedArray=(40)
#declare -a nSeedArray=(20 30 40)

# just for testing
#declare -a nYearArray=(0)

for ll in "${!projectionDirectories[@]}" 
do

    #projectionNumber=0
    projectionNumber=$ll

    baseInputDir="${baseInputDir_pre}/${projectionDirectories[$projectionNumber]}"

    # "https://stackoverflow.com/questions/52275988/populate-an-array-with-list-of-directories-existing-in-a-given-path-in-bash"
    modelDirArray=($baseInputDir/Run_*)    # This creates an array of the full paths to all subdirs



    for hh in "${!numRunsPerJobArray[@]}"
    #for hh in ${!numRunsPerJobArray[@]}
    do

        for kk in "${!nSeedArray[@]}"
        #for kk in ${!nSeedArray[@]}
        do

            numRunsPerJob=${numRunsPerJobArray[$hh]}
            nSeed=${nSeedArray[$kk]}
            experimentDir="${experimentDir_pre}_nRunsPerNode_$(printf %02d ${numRunsPerJob})_nSeed_$(printf %02d ${nSeed})"
            outputDir="${baseOutputDir}/${experimentDir}"

            echo "InputDir: ${baseInputDir}"
            echo "OutputDir: ${outputDir}"

            mkdir -p ${outputDir}/z_logs


            dayNudgeRun=$(( $nSeed*$seedSpacing ))
            #echo "$dayNudgeRun"

            dayNudgeJob=$(( $dayNudgeRun*$numRunsPerJob ))
            #echo "$dayNudgeJob"

            # Had not been allowing enough his files to be read by readers. Will also need more than 2 readers if Mesoscale can handle bigger jobs. 
            numYearsJob=$((dayNudgeJob/365+2))



            #printf '%s\n' "${modelDirArray[@]}"


            daysPerYearArray=()
            cumulativeDaysYearArray=()
            #declare -a daysPerYearArray
            #declare -a cumulativeDaysYearArray
            #cumulativeDaysYearArray+=0

            for ii in "${!modelDirArray[@]}" 
            #for ii in ${!nYearArray[@]} 
            do
                runYearArray=(${modelDirArray[ii]}/wc15n_avg_*.nc) 
                daysPerYearArray+=(${#runYearArray[@]})
            done

            #printf '%s\n' "${daysPerYearArray[@]}"

            totalDays=0
            for ii in "${!daysPerYearArray[@]}"
            #for ii in ${!daysPerYearArray[@]}
            do
                let totalDays+=${daysPerYearArray[ii]}

                sum=0

                for ((jj=0; jj<=$ii; jj++))
                do
                let sum+=${daysPerYearArray[jj]}
                done
                cumulativeDaysYearArray+=($sum)
            done

            #printf '%s\n' "${#cumulativeDaysYearArray[@]}"
            #printf '%s\n' "${#daysPerYearArray[@]}"

            #daysBeforeFinalYear=${cumulativeDaysYearArray[-2]}
            #echo "$daysBeforeFinalYear"


            lastSeedDay=$(( totalDays-driftDays ))
            #lastSeedDay=$(( totalDays-90 ))

            #echo "$totalDays"
            #echo "$lastSeedDay"

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

            #for (( ii = 0 ; ii <= numJobs ; ii ++  )); 
            for (( ii = 0 ; ii <1 ; ii ++  ));  # FOR TESTING - JUST RUN ONCE 
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

                #echo "$runYear"

                #echo "${#cumulativeDaysYearArray[$runYear]}"
                #printf '%s\n' "${cumulativeDaysYearArray[@]}"

#                echo "$dayNudge"
#                echo "${cumulativeDaysYearArray[runYear]}"
#                echo "$runYear"
#                echo ""

                if (( $dayNudge > ${cumulativeDaysYearArray[runYear]} )); then
                    for (( gg = $runYear; gg < ${#modelDirArray[@]}; gg ++));
                    do
                        if (($dayNudge > ${cumulativeDaysYearArray[gg]})); then
                            runYear=$((runYear+1))
                        else
                            break
                        fi
                    done
                    #runYear=$((runYear+1))
                fi
                
#                echo "$dayNudge"
#                echo "${cumulativeDaysYearArray[runYear]}"
#                echo "$runYear"
#                echo ""
#                echo ""


                #unset startNudgeArray
                #declare -a startNudgeArray
                startNudgeArray=()
                for (( jj = 0; jj < $numRunsPerJob; jj ++));
                do
                    currentNudge=$((dayNudge + dayNudgeRun*jj))
                    if (( ($currentNudge + $dayNudgeRun - $seedSpacing) > $lastSeedDay  )); then
                        break
                    fi
                    startNudgeArray+=($currentNudge)
                done

                if (( ${#startNudgeArray} == 0  )); then
                    break
                fi

                ### Referencing this array: modelDirArray=($baseInputDir/Run_*)    # This creates an array of the full paths to all subdirs


                runYear0=0
                #for gg in ${!cumulativeDaysYearArray[@]};  
                for cumulativeDays in "${cumulativeDaysYearArray[@]}";  
                #for cumulativeDays in ${cumulativeDaysYearArray[@]};  
                do

                    #if ((${startNudgeArray[0]} > ${cumulativeDaysYearArray[$gg]})); then 
                    if ((${startNudgeArray[0]} > $cumulativeDays)); then 
                        runYear0=$((runYear0 + 1)); 
                    else
                        break
                    fi
                done
                
                #echo "year0:"
                #echo ""
                #echo "$runYear0"
                #echo ""
                #echo "arrayVal:"
                #echo "${cumulativeDaysYearArray[runYear0]}"
                #echo ""


                runYear=$runYear0

                singleDirSwitchArray=()
                jobDirArray=()
                for nudge in "${startNudgeArray[@]}";
                #for nudge in ${startNudgeArray[@]};
                #for gg in ${!startNudgeArray[@]};
                #for (( gg = $runYear0; gg < ${#startNudgeArray[@]}; gg ++));
                do

                    if (($runYear < ${#modelDirArray[@]})); then
                        

                        if (($nudge > ${cumulativeDaysYearArray[$runYear]})); then 
                            runYear=$((runYear+1))
                        #echo "$runYear"
                        fi
                    fi
                    if (($runYear+1 == ${#modelDirArray[@]})); then
                        singleDirSwitchArray+=(1)
                    else
                        singleDirSwitchArray+=(0)
                    fi
                    
                    #echo "$nudge"

                    jobDirArray+=(${modelDirArray[$runYear]})

                done
                

                #echo "nudgeVal:"
                #printf '%s\n' "${startNudgeArray[0]}"
                
                #echo ""
                #printf '%s\n' "${singleDirSwitchArray[@]}"
                #printf '%s\n' "${startNudgeArray[@]}"
                #echo ""
                #echo "$totalDays"
                #echo "$lastSeedDay"
                #echo ""
                #printf '%s\n' "${jobDirArray[@]}"

                #echo "${#startNudgeArray[@]}"
                #echo ""
                #echo ""
                #echo ""

                echo "Hi 1"

                #./a_call_slurm.sh dtCalc=$dtCalc dtSave=$dtSave bufferLength=$bufferLength nSeed=$nSeed outputDir=$outputDir jobDirArray="${jobDirArray[@]}" startNudgeArray="${startNudgeArray[@]}" singleDirSwitchArray="${singleDirSwitchArray[@]}" &
                #. ./a_call_slurm.sh "$dtCalc" "$dtSave" "$bufferLength" "$nSeed" "$outputDir" "${jobDirArray[@]}" "${startNudgeArray[@]}" "${singleDirSwitchArray[@]}" &
                . ./a_call_slurm.sh $dtCalc $dtSave $bufferLength $nSeed $outputDir "jobDirArray[@]" "startNudgeArray[@]" "singleDirSwitchArray[@]" &

                echo "Hi 2"


#                if ((${#startNudgeArray[@]} > 0 )); then
                    #./a_call_slurm.sh $dtCalc $dtSave $bufferLength $nSeed $readerDir1 $readerDir2 $outputDir "${startNudgeArray[@]}" &
#                fi

                # I think I need to add a sleep call here, to make sure my script catches new runs and doesn't
                # create too many slurm jobs
                
                #sleep 10

            done
        done
    done
done






