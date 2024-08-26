#!/bin/bash

dtCalc=$1
dtSave=$2
bufferLength=$3
nSeed=$4

# From https://stackoverflow.com/questions/17219453/bash-command-line-arguments-into-an-array-and-subset-the-array-based-on-the-para
# Notice the 5 below... that should be the number after the last parameter number above (currently 4, from nSeed=$4)
startNudgeArray=("${@:5:$1}")

nRuns=${#startNudgeArray[@]}

parentDir=$(pwd)

runString="dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength},parentDir=${parentDir},nSeed=${nSeed},startNudgeArray=\"${startNudgeArray[@]}\",nRuns=${nRuns}"

# Look for LAST log of the multi-run parallel slurm job
logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})_$(printf %03d ${startNudgeArray[${#startNudgeArray[@]}-1]})"
#logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})_$(printf %03d ${startNudgeArray[0]})"
#logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})"

#echo -e "\n"
#echo "$logString"


#job_num_pre=$(sbatch --export="ALL,${runString}" a_run_opendrift_controller_parallel_test.sh)
job_num_pre=$(sbatch --export="ALL,${runString}" a_run_opendrift_controller_parallel.sh)

job_num_split=($job_num_pre)
jobId=${job_num_split[-1]}

while [ ! -f z_output/log_${logString}.txt ]; do
    #sleep 300 # The production sleep value here should relate to the sum of delays imposed on the starts of the parallel runs (see the the "run" script)
    sleep 20
done

mv slurm-*.out s_slurm_output/ 2>/dev/null; true

# Now change logString to be the name of the LAST log; stop tracking memory when the final run is over
logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})_$(printf %03d ${startNudgeArray[${#startNudgeArray[@]}-1]})"

memFileString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})"

while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
    if [ ! -f z_output/log_${logString}.txt ]; then
        break
    fi
    sleep 10 
   
    arr=()
    while read -r line; do
        arr+=("$line")
    done <<< "$(sstat -p --format=maxrss ${jobId}.batch)" 
    #echo ${arr[1]:0:-1} >> z_output/run_memory_info_${logString}.txt
    echo ${arr[1]:0:-1} >> z_output/run_memory_info_${memFileString}.txt
done



