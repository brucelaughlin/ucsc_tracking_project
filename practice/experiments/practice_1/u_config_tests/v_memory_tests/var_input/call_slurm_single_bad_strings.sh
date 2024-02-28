#!/bin/bash

# Provide input arguments, currently $1 = number of floats, no other input for now

numFloats=$1
dtCalc=60
dtSave=60

runString="numFloats=${numFloats},dtCalc=${dtCalc},dtSave=${dtSave}"
logString="${numFloats}_${dtCalc}_${dtSave}"

#sbatch --export="ALL,${runString}" run_single.sh >> job_strings_slurm.txt
sbatch --export="ALL,${runString}" run_single_limitFloats.sh >> job_strings_slurm.txt

sleep 5

jobId=$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}')

sleep 20
while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
    sleep 10 
    #sstat --format=jobId,maxrss,averss,MaxVMsize ${jobId}.batch >> z_output/run_memory_info_${logString}.txt
    #sstat -p --format=maxrss ${jobId}.batch >> z_output/run_memory_info_${logString}.txt
    #memString_pre=$(sstat -p --format=maxrss ${jobId}.batch) 
   
    arr=()
    while read -r line; do
        arr+=("$line")
    done <<< "$(sstat -p --format=maxrss ${jobId}.batch)" 
    echo ${arr[1]:0:-1} >> z_output/run_memory_info_${logString}.txt
    #${arr[1]:0:-1} >> z_output/run_memory_info_${logString}.txt
    #${arr[1]::-1} >> z_output/run_memory_info_${logString}.txt
done



