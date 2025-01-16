#!/bin/bash

#SBATCH --job-name opendrift
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd "$callingDear"

#----------------------------------------------------------------------------------------------------------------
# So I think here I need to loop over the number of "job directories" specified in the config file
#----------------------------------------------------------------------------------------------------------------
# THIS FEELS SO HACK-Y
# So, our config file needs to always have the same order of dictionary keys, since my hacked solution below
# relies on it
jobDirList=($(sed 's/[.-]//g' <<< $(awk '/jobDirList/,/numberOfSeeds/' $configFile)))
jobDirList=("${jobDirList[@]:1:${#jobDirList[@]}-3}")
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

for jobRunNum in "${!jobDirList[@]}"; do

    logFilePre="${configFile/.config.yaml/}_configFileNum_$(printf %02d ${configFileNum})_configFileJob_$(printf %02d ${jobRunNum}).driftlog"
    logFile="${runDir}/z_logs/$(basename $logFilePre)"

    #echo "hi" > $logFile
    #echo "$logfile"

    echo "$(hostname)" > "$logFile"

    #python opendrift_run_store_eco_variables_240830_memTest_configFile_dielMigration_v1.py --configfile $configFile --jobrunnumber $jobRunNum &>> "$logFile" &
    #python opendrift_run_store_eco_variables_240830_memTest_configFile_v2.py --configfile $configFile --jobrunnumber $jobRunNum &>> "$logFile" &
    python opendrift_run_store_eco_variables_240830_memTest_configFile_jordanaEx_v1.py --configfile $configFile --jobrunnumber $jobRunNum &>> "$logFile" &

done
wait # I don't know why I was using "wait" here.  I think the "&" above is required to make the python calls run in parallel

