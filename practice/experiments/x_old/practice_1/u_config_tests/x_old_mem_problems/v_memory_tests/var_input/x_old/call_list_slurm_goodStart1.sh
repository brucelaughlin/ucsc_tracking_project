#!/bin/bash

jobArray=()
numArray=()

#for n in 1 2 5 10 50 80;
#for n in 1 10 100 1000 10000;
for n in 1 10;
do
    sbatch --export="ALL,numFloats=$n,dtCalc=60,dtSave=60" run_all.sh >> job_strings_slurm.txt

    jobid=$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}')

    jobArray+=($jobid)
    numArray+=($n)
    

done


#for id in "${jobArray}";
for id in "${!jobArray[@]}";
do
    
    #sstat --format=jobid,maxrss,averss,MaxVMsize ${id}.batch >> run_info_
    sstat --format=jobid,maxrss,averss,MaxVMsize ${jobArray[id]}.batch >> z_output/run_memory_info_${numArray[id]}.txt

done



