#!/bin/bash

job_num_pre="Submitted batch job 801393"
job_num_split=($job_num_pre)
jobId=${job_num_split[-1]}

echo $jobId

