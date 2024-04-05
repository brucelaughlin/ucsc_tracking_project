#!/bin/bash

# Need to modify opendrift caller python script: last run 90 days before end of last year

# Should pass year to script, so script initiates reader for entire year and entire next year.
# And if in final year, don't try to load next year

# Use Jerome's files to send Year and Day to the opendrift caller; within the caller,
# make the datetime starting date



# I think I can run 4 months of seeds at a time.  Still finishing tests on memory usage as function of number of seeds


############################################################
# Modify this each time, so you don't overwrite past results
############################################################

runOutputDir="run_240403"

############################################################





dtCalc=60

dtSave=720

bufferLength=100 # default, but must be provided in my code

#baseInputDir="/data03/fiechter/WC15N_1988-2010/"
baseInputDir="/data03/fiechter/WC15N_1988-2010"

baseOutputDir="/data03/blaughli/tracking_project_output"


outputDir=$baseOutputDir/$runOutputDir

# "https://stackoverflow.com/questions/52275988/populate-an-array-with-list-of-directories-existing-in-a-given-path-in-bash"
runDirArray=($baseInputDir/Run_*/)    # This creates an array of the full paths to all subdirs
runDirArray=("${runDirArray[@]%/}")    # This removes the trailing slash on each item

# for testing, only use first year
#runDirArray=("${runDirArray[@]:0:1}")


#printf '%s\n' "${runDirArray[@]}"

finalYearFlag=0

#dayNumber=1

#numDays=0

#for ii in "${runDirArray[@]}"
for ii in "${!runDirArray[@]}"
do
    runYearArray=(${runDirArray[ii]}/wc15n_avg_*.nc) #Array of all the filenames within the year directory (just used to get day number)
    #runYearArray=($ii/wc15n_avg_*.nc) #Array of all the filenames within the year directory (just used to get day number)

    #numDays=$((numDays+${#runYearArray[@]}))
            

        
        # Check if we're in the final year
        if (( $ii+1 == ${#runDirArray[@]} )); then
            finalYearFlag=1
        fi




    for jj in "${!runYearArray[@]}" # The "!" gives us jj as the array index (integer from 0 to 364 or 365)
    do
        
        
        #if [ "$jj" = "${runYearArray[0]}" ]; then
        if [ $jj = 365 ]; then
            echo $jj
        fi

        if ; then
            break
        fi
       
        
        #./a_call_slurm_varInputFile.sh $dtCalc $dtSave $bufferLength $ii $jj $finalYearFlag &


    done    

done





