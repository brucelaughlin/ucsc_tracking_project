#!/bin/bash

dtCalc=$1
dtSave=$2
bufferLength=$3
numFloats=$4
#dtCalc=60
#dtSave=60
#bufferLength=100
#numFloats=9528

runString="numFloats=${numFloats},dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength}"
#logString="$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})_$(printf %03d ${bufferLength})"
logString="$(printf %06d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})_$(printf %03d ${bufferLength})"

#job_num_pre=$(sbatch --export="ALL,${runString}" a_runSingle.sh)
job_num_pre=$(sbatch --export="ALL,${runString}" a_runSingle_setEnvMalloc.sh)
job_num_split=($job_num_pre)
jobId=${job_num_split[-1]}

#while [ ! -f log_${logString}.txt ]; do
while [ ! -f z_output/log_${logString}.txt ]; do
    sleep 20
done

#mv slurm-*.out s_slurm_output/ 2>/dev/null; true

while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
#while [[ $(tail -n 1 log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
    if [ ! -f z_output/log_${logString}.txt ]; then
    #if [ ! -f log_${logString}.txt ]; then
        break
    fi
    sleep 10 
   
    arr=()
    while read -r line; do
        arr+=("$line")
    done <<< "$(sstat -p --format=maxrss ${jobId}.batch)" 
    echo ${arr[1]:0:-1} >> z_output/run_memory_info_${logString}.txt
    #echo ${arr[1]:0:-1} >> run_memory_info_${logString}.txt
done



