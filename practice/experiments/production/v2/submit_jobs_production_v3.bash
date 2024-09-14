#!/bin/bash

# v3: the serialSize thing is not quite right - we're not always using all nodes.  Maybe round down?

# first generate config file for all jobs with the python script



callingDir="$(pwd)"

# Set the number of nodes to use for the job (8 seems ok.. everyone else uses 8!)
#numNodes=9 # just works out that we have 18 jobs for now, so 9 splits them evenly between current and queued jobs
#numNodes=10
numNodes=12

runBaseDir="/data/blaughli/tracking_project_output_projections/production_n15_s20"

# This directory is populated by running the python script that generates the config files
runDirs=($runBaseDir/*)
    
extraArgs=""

for ii in "${!runDirs[@]}"
do

    runDir=${runDirs[$ii]}

    configFiles=($runDir/z_config_files/*)

    numFiles=${#configFiles[@]}

    # rounding up
    serialSize=$(( ($numFiles+$numNodes-1)/$numNodes ))
    #serialSize=$(( (${#configFiles[@]}+$numNodes-1)/$numNodes ))

    # Store the number of files we want processed at the $serialSize (the rest we'll run at $serialSize-1)
    nMaxSerial=$(( $numNodes*(1-$serialSize)+$numFiles ))

    counterRun=0
    counterNode=0

#    extraArgs=""

    for jj in "${!configFiles[@]}"; 
    do

        (( counterRun ++ ))

        configFile=${configFiles[$jj]}
       
        configFileNum=$jj

        jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,configFileNum=$configFileNum,runDir=$runDir" $extraArgs sbatch_call_v2.bash) 

        # For testing, maybe use extraArgs="--afterok", which will kill the whole job if something fails.  but that will help with time wasted monitoring.          
        # For production, use "--afterany", so that if a single job fails, can re-run later using the config file (that's part of the beauty of the config file approach)
        
        extraArgs="-d afterany:$jobNum"                                                                                                                               
        #extraArgs="-d afterok:$jobNum"                                                                                                                               
                                                                                                                                                                         
        if [[ $counterRun == $serialSize ]]; then                                                                                                                           
            counterRun=0                                                                                                                                                    
            extraArgs=""
            (( counterNode ++ )) 
            if [[ $counterNode == $nMaxSerial ]]; then
                (( serialSize -- ))
            fi           
        fi                                                                                                                                                               
        
    done
done

