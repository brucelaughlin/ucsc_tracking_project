#!/bin/bash

for id in "${!jobArray[@]}";
    while [[ $(tail -n 1 z_output/run_memory_info_${numArray[id]}.txt | awk '{print $NF}') != Finished ]]; do
    #while [[ $(tail -n 1 z_output/run_memory_info_${numArray[id]}.txt | awk '{print $NF}') != "Finished" ]]; do
    #while [$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}') -eq "Finished"]; do
        sleep 10
        sstat --format=jobid,maxrss,averss,MaxVMsize ${jobArray[id]}.batch >> z_output/run_memory_info_${numArray[id]}.txt
done


# This works (below)!?

##while [[ $(tail -n 1 z_output/run_memory_info_${numArray[id]}.txt | awk '{print $NF}') != "Finished" ]]; do
#if [[ $(tail -n 1 z_output/log_1_60_60.txt | awk '{print $NF}') != "Finished" ]]; then
if [[ $(tail -n 1 z_output/log_1_60_60.txt | awk '{print $NF}') == "Finished" ]]; then
#while [$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}') -eq "Finished"]; do
    #sleep 10
    #sstat --format=jobid,maxrss,averss,MaxVMsize ${jobArray[id]}.batch >> z_output/run_memory_info_${numArray[id]}.txt
    echo working
fi
#done



