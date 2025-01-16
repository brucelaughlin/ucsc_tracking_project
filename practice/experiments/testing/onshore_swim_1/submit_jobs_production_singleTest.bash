#!/bin/bash

# v3: the serialSize thing is not quite right - we're not always using all nodes.  Maybe round down?

# first generate config file for all jobs with the python script



callingDir="$(pwd)"

# Set the number of nodes to use for the job (8 seems ok.. everyone else uses 8!)
#numNodes=9 # just works out that we have 18 jobs for now, so 9 splits them evenly between current and queued jobs

#numNodes=7
#numNodes=10
#numNodes=12
#numNodes=9
#numNodes=18
numNodes=1

runBaseDir="/data/blaughli/tracking_output/swim_tests"
#runBaseDir="/data/blaughli/tracking_output/baseYear_2071"

# This directory is populated by running the python script that generates the config files
runDirs=($runBaseDir/dummy_dir_onshoreSwim_test)
#runDirs=($runBaseDir/WC15N_1988-2010_onshoreSwim_test)
##runDirs=($runBaseDir/WC15N_GFDLTV_onshoreSwim_test)
#runDirs=($runBaseDir/*)
    
extraArgs=""

numFiles=0

# Need to determine "serialSize" and "numNodesAtMaxSerial" before starting the main loop
for ii in "${!runDirs[@]}"
do
    runDir=${runDirs[$ii]}
    configFiles=($runDir/z_config_files/*)
    (( numFiles+=${#configFiles[@]} ))
done 


serialSize=$(( ($numFiles+$numNodes-1)/$numNodes ))
# Store the number of nodes we want run with $serialSize files (the rest we'll run at $serialSize-1 files)
numNodesAtMaxSerial=$(( $numNodes*(1-$serialSize)+$numFiles ))


counterRun=0
counterNode=0

for ii in "${!runDirs[@]}"
do

    runDir=${runDirs[$ii]}

    configFiles=($runDir/z_config_files/*)

    #numFiles=${#configFiles[@]}

    # rounding up
    #serialSize=$(( ($numFiles+$numNodes-1)/$numNodes ))

    # Store the number of files we want processed at the $serialSize (the rest we'll run at $serialSize-1)
    #numNodesAtMaxSerial=$(( $numNodes*(1-$serialSize)+$numFiles ))

#    counterRun=0
#    counterNode=0

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
            if [[ $counterNode == $numNodesAtMaxSerial ]]; then
                (( serialSize -- ))
            fi           
        fi                                                                                                                                                               
        
    done
done

