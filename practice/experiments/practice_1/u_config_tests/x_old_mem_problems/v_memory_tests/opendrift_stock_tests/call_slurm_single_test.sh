#!/bin/bash

# Provide input arguments, currently $1 = number of floats, no other input for now

numFloats=$1
dtCalc=$2
dtSave=$3
bufferLength=$4
#dtCalc=60
#dtSave=60

#runString="numFloats=${numFloats},dtCalc=${dtCalc},dtSave=${dtSave}"
runString="numFloats=${numFloats},dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength}"
#logString="$(printf %05d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})"
logString="$(printf %05d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})_$(printf %03d ${bufferLength})"

#sbatch --export="$(ALL,${runString})" run_single.sh >> job_strings_slurm.txt
job_num_pre=$(sbatch --export="ALL,${runString}" run_single_test.sh)
job_num_split=($job_num_pre)
jobId=${job_num_split[-1]}

#echo $jobId

while [ ! -f z_output/log_${logString}.txt ]; do
    sleep 20
done

mv slurm-*.out s_slurm_output/ 2>/dev/null; true

while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
    if [ ! -f z_output/log_${logString}.txt ]; then
        break
    fi
    sleep 10 
    #sleep 5 
   
    arr=()
    while read -r line; do
        arr+=("$line")
    done <<< "$(sstat -p --format=maxrss ${jobId}.batch)" 
    echo ${arr[1]:0:-1} >> z_output/run_memory_info_${logString}.txt
done



