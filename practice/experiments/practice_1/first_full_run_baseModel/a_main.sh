#!/bin/bash

dtCalc=60

dtSave=60

bufferLength=100 # default, but must be provided in my code

#baseInputDir="/data03/fiechter/WC15N_1988-2010/"
baseInputDir="/data03/fiechter/WC15N_1988-2010"

# "https://stackoverflow.com/questions/52275988/populate-an-array-with-list-of-directories-existing-in-a-given-path-in-bash"
runDirArray=($baseInputDir/Run_*/)    # This creates an array of the full paths to all subdirs
runDirArray=("${runDirArray[@]%/}")    # This removes the trailing slash on each item

# for testing, only use first year
runDirArray=("${runDirArray[@]:0:1}")


#printf '%s\n' "${runDirArray[@]}"

dayNumber=1

numDays=0

for ii in "${runDirArray[@]}"
do
    runYearArray=($ii/wc15n_avg_*.nc)
    #echo "${runYearArray[0]}"
    #echo "${runYearArray[-1]}"
    #echo "$ii"

    # For testing, slice array, keep only the first few days of output
    #runYearArray=("${runYearArray[@]:0:4}")

    numDays=$((numDays+${#runYearArray[@]}))

    #for jj in "${runYearArray[@]}"
    for jj in "${!runYearArray[@]}" # The "!" gives us jj as the array index (integer)
    do
        
        #if [ "$jj" = "${runYearArray[0]}" ]; then
        if [ $jj = 365 ]; then
            echo $jj
        fi
       
        
        #./a_call_slurm_varInputFile.sh $dtCalc $dtSave $bufferLength $jj &


    done    

done





