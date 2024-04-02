#!/bin/bash

# Need to modify opendrift caller python script: last run 90 days before end of last year

# Should pass year to script, so script initiates reader for entire year and entire next year.
# And if in final year, don't try to load next year

# Use Jerome's files to send Year and Day to the opendrift caller; within the caller,
# make the datetime starting date

dtCalc=60

dtSave=60

bufferLength=100 # default, but must be provided in my code

#baseInputDir="/data03/fiechter/WC15N_1988-2010/"
baseInputDir="/data03/fiechter/WC15N_1988-2010"

# "https://stackoverflow.com/questions/52275988/populate-an-array-with-list-of-directories-existing-in-a-given-path-in-bash"
runDirArray=($baseInputDir/Run_*/)    # This creates an array of the full paths to all subdirs
runDirArray=("${runDirArray[@]%/}")    # This removes the trailing slash on each item

# for testing, only use first year
#runDirArray=("${runDirArray[@]:0:1}")


#printf '%s\n' "${runDirArray[@]}"

finalYearFlag=0

nodeLimitPlusOne=5 # set to 1 higher than max number of nodes to use

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
       
        while [ $(squeue -u blaughli -h -t running | wc -l) -lt $nodeLimitPlusOne ]; do
           sleep 20
       done 
        
        #if [ "$jj" = "${runYearArray[0]}" ]; then
        
        #if [ $jj = 365 ]; then
        #    echo $jj
        #fi

         
        numNodesUsed=$(squeue -u blaughli -h -t running | wc -l) # This returns the number of runnings jobs.  So, continue if not at our chosen max number of nodes
        
        if ; then
            break
        fi
       
        
        #./a_call_slurm_varInputFile.sh $dtCalc $dtSave $bufferLength $ii $jj $finalYearFlag &


    done    

done





