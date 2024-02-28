#!/bin/bash


dtCalc=60
dtSave=60

jobArray=()
numArray=()
logArray=()


#for n in 1 10 100 1000 10000;
#for n in 1 10;
for n in 1; do
    numFloats=$n
    runString="numFloats=${numFloats},dtCalc=${dtCalc},dtSave=${dtSave}"
    logString="${numFloats}_${dtCalc}_${dtSave}"

    #sbatch --export="ALL,numFloats=$n,dtCalc=60,dtSave=60" run_all.sh >> job_strings_slurm.txt
    sbatch --export="ALL,${runString}" run_all.sh >> job_strings_slurm.txt

    jobid=$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}')

    jobArray+=($jobid)
    numArray+=($n)
    

done


#for id in "${jobArray}";
for id in "${!jobArray[@]}"; do
    sleep 20
    #while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
    while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
        #sleep 10
        #sstat --format=jobid,maxrss,averss,MaxVMsize ${jobArray[id]}.batch >> z_output/run_memory_info_${numArray[id]}.txt
        sleep 10 &
        sstat --format=jobid,maxrss,averss,MaxVMsize ${jobArray[id]}.batch >> z_output/run_memory_info_${numArray[id]}.txt &
    done
done



