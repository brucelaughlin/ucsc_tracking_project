#!/bin/bash

operatingDir="$(pwd)"

configFile="config.yaml"
jobRunNum=0
logFile="z_testLog.txt"

# first generate config file for all jobs with python

# might want to name those ".config" vs ".yaml", or some mix... vi might even be able to see they're yaml

# if you really want to hardcode the list of config files, can ls -1  to get a list of all files (not ls -l)




#iterate over the config files with *

#might need counter variable

# in here also have the max node checking


# can pass job name to this call, overwriting "job-name' in the sbatch script

configFiles=(
config1.yaml
config2.yaml
config3.yaml
config4.yaml
config5.yaml
config6.yaml
config7.yaml
)

numNodes=2

# Rounding up
serialSize=$(( (${#configFiles[@]}+$numNodes-1)/$numNodes ))

counter=0

extraArgs=""

for configFile in "${configFiles[@]}"; 
do
    
    (( counter ++ ))

    logFile="${configFile/yaml/}driftlog"

    echo "sbatch --parseable $configFile $extraArgs"
    #echo "sbatch --parseable $configFile $extraArgs" &> $logFile   # replace this line
    jobNum=$(($counter+42))                # and this
    
    # For testing, maybe use extraArgs="--aftersuccess", which will kill the whole job if something fails.  but that will help with time wasted monitoring.
    # For production, use "--afterany", so that if a single job fails, can re-run later using the config file (that's part of the beauty of the config file approach)
    extraArgs="--aftersuccess=$jobNum"
    #extraArgs="--afterany=$jobNum"
    
    if [[ $counter == $serialSize ]]; then
        counter=0
        extraArgs=""
    fi


done


#sbatch $extraArgs --chdir="$operatingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash



#sbatch --chdir="$operatingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash

#job_num_pre=$(sbatch --parseable --chdir="$operatingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash)



