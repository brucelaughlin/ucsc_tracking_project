#!/bin/bash

jobArray=()
numArray=()

#for n in 1 10 100 1000 10000;
#for n in 1 10;
for n in 1; do
    sbatch --export="ALL,numFloats=$n,dtCalc=60,dtSave=60" run_all.sh >> job_strings_slurm.txt

    jobid=$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}')

    jobArray+=($jobid)
    numArray+=($n)
    

done


#for id in "${jobArray}";
for id in "${!jobArray[@]}";
    while [[ $(tail -n 1 z_output/run_memory_info_${numArray[id]}.txt | awk '{print $NF}') != Finished ]]; do
    #while [[ $(tail -n 1 z_output/run_memory_info_${numArray[id]}.txt | awk '{print $NF}') != "Finished" ]]; do
    #while [$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}') -eq "Finished"]; do
        sleep 10
        sstat --format=jobid,maxrss,averss,MaxVMsize ${jobArray[id]}.batch >> z_output/run_memory_info_${numArray[id]}.txt
done



