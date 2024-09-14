#!/bin/bash

callingDir="$(pwd)"

# first generate config file for all jobs with python

# might want to name those ".config" vs ".yaml", or some mix... vi might even be able to see they're yaml

# if you really want to hardcode the list of config files, can ls -1  to get a list of all files (not ls -l)




#iterate over the config files with *

#might need counter variable

# in here also have the max node checking


# can pass job name to this call, overwriting "job-name' in the sbatch script

#runBaseDir="/data/blaughli/tracking_project_output_projections/production"
runBaseDir="/data/blaughli/tracking_project_output_projections/memory_tests"
#runBaseDir="/data/blaughli/tracking_project_output_projections/memory_tests_32node"
#runBaseDir="/data/blaughli/tracking_project_output_projections/memory_tests_32v1_race"

# This directory is populated by running the python script that generates the config files
runDirs=($runBaseDir/*)

#testArr=(1)

for ii in "${!runDirs[@]}"
#for ii in "${!testArr[@]}"
do

    runDir=${runDirs[$ii]}
    #runDir=$runBaseDir/${runDirs[$ii]}


    configFiles=($runDir/z_config_files/*)

    #echo "$runDir"

    # ------------------------------------------------------------
    # ------------------- for production -------------------------
    # (Want to run in serial, unlike before - so just a single job...)

    #numNodes=2

    ## Rounding up
    #serialSize=$(( (${#configFiles[@]}+$numNodes-1)/$numNodes ))
    # ------------------------------------------------------------
    
    #counter=0

    extraArgs=""

    for jj in "${!configFiles[@]}"; 
    #for jj in "${!testArr[@]}"
    do
        configFile=${configFiles[$jj]}
       
        #jobRunNum=$jj
        configFileNum=$jj

        #echo "$configFile"

        #echo "$jj"

        #(( counter ++ ))
       
        #slurmOutFilePre="slurmInfo_runDir_$(printf %02d ${ii})_configFile_$(printf %02d ${jj}).out"
        #slurmOutFile="${runDir}/z_slurmOut/$(basename $slurmOutFilePre)"

        #logFilePre1="${configFile/config.yaml/}driftlog"
        ###logFilePre="${configFile/.config.yaml/}_$(printf %02d ${jobRunNum})_.driftlog"
        ###logFile="${configFile/yaml/}driftlog"

        #logFilePre2="${runDir}/z_logs/$(basename $logFilePre1)"

        #echo "$logFile"

        #echo "$callingDir"

        #echo "sbatch --parsable $configFile $extraArgs"
        ##echo "sbatch --parsable $configFile $extraArgs" &> $logFile   # replace this line
        
        #echo "sbatch --parsable --chdir="$callingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash"
        
        ##jobNum=$(($counter+42))                # and this
        
        
        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,configFileNum=$configFileNum,runDir=$runDir" --output="$slurmOutFile" sbatch_call.bash) 
        jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,configFileNum=$configFileNum,runDir=$runDir" sbatch_call.bash) 



        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,configFileNum=$configFileNum" --output="$slurmOutFile" sbatch_call.bash)                
        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,logFilePre=$logFilePre2,configFileNum=$configFileNum" --output="$slurmOutFile" sbatch_call.bash)                
        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir,logFile=$logFilePre2,configFileNum=$configFileNum" sbatch_testCall.bash)                
        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,callingDir=$callingDir" --output="$logFile" sbatch_testCall.bash)                
        
        #jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum,callingDir=$callingDir" --output="$logFile" sbatch_testCall.bash)                
        
        
        ####jobNum=$(sbatch --parsable --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash)                
        ####jobNum=$(sbatch --parsable --chdir="$callingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash)                
        
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

