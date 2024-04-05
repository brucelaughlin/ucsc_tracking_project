#!/bin/bash

# The compression call from within the python script works!  see the "compress_test" directory.

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


maxNodes=8


#dtCalc=60
dtCalc=1440 # test value

#dtSave=720
dtSave=1440 # test value

bufferLength=100 # default, but must be provided in my code

#baseInputDir="/data03/fiechter/WC15N_1988-2010/"
baseInputDir="/data03/fiechter/WC15N_1988-2010"

baseOutputDir="/data03/blaughli/tracking_project_output/"


runOutputDir="test1/"


outputDir="${baseOutputDir}${runOutputDir}"

# "https://stackoverflow.com/questions/52275988/populate-an-array-with-list-of-directories-existing-in-a-given-path-in-bash"
runDirArray=($baseInputDir/Run_*/)    # This creates an array of the full paths to all subdirs
runDirArray=("${runDirArray[@]%/}")    # This removes the trailing slash on each item

# for testing, only use first year
#runDirArray=("${runDirArray[@]:0:1}")

# for testing, only use first TWO years
runDirArray=("${runDirArray[@]:0:2}")
#echo "${runDirArray[*]}"
#printf '%s\n' "${runDirArray[@]}"


#printf '%s\n' "${runDirArray[@]}"

#declare -a monthSeedArray=(
#[0]=0
#[1]=2
#[2]=4
#[3]=6
#[4]=8
#[5]=10
#)

#monthSeedArray=(0 2 4 6 8 10)
monthSeedArray=(0 3 6 9)

baseYear=1988

finalYearFlag=0

#for ii in "${runDirArray[@]}"
for ii in "${!runDirArray[@]}"
do

    # Compute the "yearNudge" (years since baseYear)
    IFS='_' read -ra yearStringArray <<< ${runDirArray[ii]}
    yearNudge=$((${yearStringArray[-1]}-$baseYear))


    # Check if we're in the final year - if so, wanna NOT seed anything that'll ask for data we don't have.
    if (( $ii+1 == ${#runDirArray[@]} )); then

        finalYearFlag=1

        unset monthSeedArray[$[${#monthSeedArray[@]}-1]]
    
        for jj in ${monthSeedArray[@]}; do
            while [ $(squeue -u blaughli -h -t running | wc -l) -gt $maxNodes ]; do
                sleep 20
            done
            ./a_call_slurm_varMonth.sh $dtCalc $dtSave $bufferLength $outputdir $yearNudge  $jj $finalYearFlag &
        done   

    elif

        for jj in ${monthSeedArray[@]}; do

            while [ $(squeue -u blaughli -h -t running | wc -l) -gt $maxNodes ]; do
                sleep 20
            done
            ./a_call_slurm_varMonth.sh $jj &


        done   
   
    fi 

done





