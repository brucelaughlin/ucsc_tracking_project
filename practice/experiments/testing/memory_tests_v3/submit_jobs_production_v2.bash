#!/bin/bash

# first generate config file for all jobs with the python script



callingDir="$(pwd)"

# Set the number of nodes to use for the job (8 seems ok.. everyone else uses 8!)
numNodes=8

runBaseDir="/data/blaughli/tracking_project_output_projections/production_test_n15_s20"
#runBaseDir="/data/blaughli/tracking_project_output_projections/production"

# This directory is populated by running the python script that generates the config files
#runDirs=("$runBaseDir/*")
runDirs=($runBaseDir/*)

for ii in "${!runDirs[@]}"
do

    runDir=${runDirs[$ii]}

    configFiles=($runDir/z_config_files/*)

    # rounding up
    serialSize=$(( (${#configFiles[@]}+$numNodes-1)/$numNodes ))

    counter=0

    extraArgs=""

    for jj in "${!configFiles[@]}"; 
    do

        (( counter ++ ))

        configFile=${configFiles[$jj]}
       
        configFileNum=$jj


        jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,configFileNum=$configFileNum,runDir=$runDir" $extraArgs sbatch_call_v2.bash) 
        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,configFileNum=$configFileNum,runDir=$runDir" $extraArgs sbatch_call.bash) 


        # For testing, maybe use extraArgs="--aftersuccess", which will kill the whole job if something fails.  but that will help with time wasted monitoring.          
        # For production, use "--afterany", so that if a single job fails, can re-run later using the config file (that's part of the beauty of the config file approach)
        
        extraArgs="-d afterok:$jobNum"                                                                                                                               
        
        #extraArgs="--aftersuccess=$jobNum"                                                                                                                               
        #extraArgs="--afterany=$jobNum"                                                                                                                                  
                                                                                                                                                                         
        if [[ $counter == $serialSize ]]; then                                                                                                                           
            counter=0                                                                                                                                                    
            extraArgs=""                                                                                                                                                 
        fi                                                                                                                                                               

        
    done
done

