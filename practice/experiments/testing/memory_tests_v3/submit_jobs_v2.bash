#!/bin/bash

# v2:  I need to iterate over the jobs specified in the config file.... 

callingDir="$(pwd)"

# first generate config file for all jobs with python

# might want to name those ".config" vs ".yaml", or some mix... vi might even be able to see they're yaml

# if you really want to hardcode the list of config files, can ls -1  to get a list of all files (not ls -l)




#iterate over the config files with *

#might need counter variable

# in here also have the max node checking


# can pass job name to this call, overwriting "job-name' in the sbatch script

runBaseDir="/data/blaughli/tracking_project_output_projections/memory_tests"

# This directory is populated by running the python script that generates the config files
runDirs=($runBaseDir/*)

testArr=(1)

#for ii in "${!runDirs[@]}"
for ii in "${!testArr[@]}"
do

    runDir=${runDirs[$ii]}
    #runDir=$runBaseDir/${runDirs[$ii]}


    #configFiles=($runDir/z_config_files/*)
   
    # There's only one config file!!! 
    #configFile=$runDir/z_config_files/*
    configFile=($runDir/z_config_files/*)

    #echo "$runDir"
    #echo "$configFile"

    # ------------------------------------------------------------
    # ------------------- for production -------------------------
    # (Want to run in serial, unlike before - so just a single job...)

    #numNodes=2

    ## Rounding up
    #serialSize=$(( (${#configFiles[@]}+$numNodes-1)/$numNodes ))
    # ------------------------------------------------------------
    
    #counter=0

    extraArgs=""
    
    # So our config file needs to always have the same order of dictionary keys    
    #jobDirList=($(awk -F'-$'  '/jobDirList/,/numberOfSeeds/' $configFile))
    jobDirList=($(awk '/jobDirList/,/numberOfSeeds/' $configFile))

    #jobDirList=("${jobDirList[@]:1}")
    #jobDirList=("${jobDirList[@]:1}")

    echo "${#jobDirList[@]}"
    echo "${jobDirList[@]}"
        
    unset "jobDirList[0]"
    unset "jobDirList[${#jobDirList}-1]"
    unset "jobDirList[${#jobDirList}-1]"
    
    echo "${jobDirList[@]}"
    
    echo "${#jobDirList[@]}"

    for jobRunNum in "${!jobDirList[@]}"; 
    do
       
        #echo "$jobRunNum"
        #echo "${jobDirList[$jobRunNum]}"

        #(( counter ++ ))

        logFilePre="${configFile/config.yaml/}driftlog"
        #logFile="${configFile/yaml/}driftlog"

        logFile="${runDir}/z_logs/$(basename $logFilePre)"

        #echo "$logFile"

        #echo "$callingDir"

        #echo "sbatch --parsable $configFile $extraArgs"
        ##echo "sbatch --parsable $configFile $extraArgs" &> $logFile   # replace this line
        
        #echo "sbatch --parsable --chdir="$callingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash"
        
        ##jobNum=$(($counter+42))                # and this
        
        
        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum,callingDir=$callingDir" --output="$logFile" sbatch_testCall.bash)                
        
        
        #echo $jobNum

        # For testing, maybe use extraArgs="--aftersuccess", which will kill the whole job if something fails.  but that will help with time wasted monitoring.
        # For production, use "--afterany", so that if a single job fails, can re-run later using the config file (that's part of the beauty of the config file approach)
        
        #extraArgs="--aftersuccess=$jobNum"
        
        ##extraArgs="--afterany=$jobNum"
        
        #if [[ $counter == $serialSize ]]; then
        #    counter=0
        #    extraArgs=""
        #fi


    done


    ###sbatch $extraArgs --chdir="$callingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash
    ###sbatch --chdir="$callingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash
    ###job_num_pre=$(sbatch --parseable --chdir="$callingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash)

done

