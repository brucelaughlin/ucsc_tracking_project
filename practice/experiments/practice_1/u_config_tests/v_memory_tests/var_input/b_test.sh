#!/bin/bash


lines=$(find . -maxdepth 1 -name "slurm-*.out" -type f)

if [ ${#lines[@]} > 0 ]; then
    mv slurm-*.out s_slurm_output/
fi
