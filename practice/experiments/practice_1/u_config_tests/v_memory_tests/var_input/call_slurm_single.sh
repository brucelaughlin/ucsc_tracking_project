#!/bin/bash

# Provide input arguments, currently $1 = number of floats, no other input for now

numFloats=$1
dtCalc=60
dtSave=60

runString="numFloats=${numFloats},dtCalc=${dtCalc},dtSave=${dtSave}"
logString="$(printf %05d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})"

sbatch --export="ALL,${runString}" run_single.sh >> job_strings_slurm.txt
#sbatch --export="ALL,${runString}" run_single_limitFloats.sh >> job_strings_slurm.txt

while [ ! -f z_output/log_${logString}.txt ]; do
    sleep 20
done

mv slurm-*.out s_slurm_output/ 2>/dev/null; true

#lines=$(find . -maxdepth 1 -name "slurm-*.out" -type f)
#if [ ${#lines[@]} > 0 ]; then
#    mv slurm-*.out s_slurm_output/
#fi

jobId=$(tail -n 1 job_strings_slurm.txt | awk '{print $NF}')

while [[ $(tail -n 1 z_output/log_${logString}.txt | awk '{print $NF}') != Finished ]]; do
    if [ ! -f z_output/log_${logString}.txt ]; then
        break
    fi
    #sleep 10 
    sleep 5 
   
    arr=()
    while read -r line; do
        arr+=("$line")
    done <<< "$(sstat -p --format=maxrss ${jobId}.batch)" 
    echo ${arr[1]:0:-1} >> z_output/run_memory_info_${logString}.txt
done



