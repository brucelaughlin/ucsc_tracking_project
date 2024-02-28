#!/bin/bash

tail -n 1 slurm_job_strings.txt | awk '{print $NF}'

