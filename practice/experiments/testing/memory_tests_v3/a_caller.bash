#!/bin/bash

operatingDir="$(pwd)"

configFile="config.yaml"
jobRunNum=0
logFile="z_testLog.txt"

# can pass job name to this call, overwriting "job-name' in the sbatch script

sbatch --chdir="$operatingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash

#job_num_pre=$(sbatch --parseable --chdir="$operatingDir" --export="ALL,configFile=$configFile,jobRunNum=$jobRunNum" --output="$logFile" sbatch_testCall.bash)



