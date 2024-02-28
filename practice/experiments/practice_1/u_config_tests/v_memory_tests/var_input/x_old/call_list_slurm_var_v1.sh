#!/bin/bash

for n in 1 2 5 10 50 80;
do
    sbatch --export="ALL,numFloats=$n,dtCalc=60,dtSave=60" run_all.sh >> slurm_job_strings.txt
done
