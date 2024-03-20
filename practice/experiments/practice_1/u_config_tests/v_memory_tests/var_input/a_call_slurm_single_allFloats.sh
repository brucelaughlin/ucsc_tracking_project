#!/bin/bash

dtCalc=$1
dtSave=$2
bufferLength=$3

runString="dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength}"
logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})"

#sbatch --export="$(ALL,${runString})" a_run_single.sh >> job_strings_slurm.txt
job_num_pre=$(sbatch --export="ALL,${runString}" a_run_single_allFloats.sh)
job_num_split=($job_num_pre)
jobId=${job_num_split[-1]}

while [ ! -f z_output/log_${logString}.txt ]; do
    sleep 20
done

mv slurm-*.out s_slurm_output/ 2>/dev/null; true

while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
    if [ ! -f z_output/log_${logString}.txt ]; then
        break
    fi
    sleep 10 
   
    arr=()
    while read -r line; do
        arr+=("$line")
    done <<< "$(sstat -p --format=maxrss ${jobId}.batch)" 
    echo ${arr[1]:0:-1} >> z_output/run_memory_info_${logString}.txt
done



