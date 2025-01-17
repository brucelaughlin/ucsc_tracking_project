#!/bin/bash

dtCalc=$1
dtSave=$2
bufferLength=$3
nSeed=$4
readerDir1=$5
readerDir2=$6
outputDir=$7

# From https://stackoverflow.com/questions/17219453/bash-command-line-arguments-into-an-array-and-subset-the-array-based-on-the-para
# Notice the 5 below... that should be the number after the last parameter number above (currently 4, from nSeed=$4)
#startNudgeArray=("${@:5:$1}")
startNudgeArray=("${@:8:$1}")

nRuns=${#startNudgeArray[@]}

parentDir=$(pwd)

#runString="dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength},parentDir=${parentDir},nSeed=${nSeed},nRuns=${nRuns},readerDir1=${readerDir1},readerDir2=${readerDir2},startNudgeArray=\"${startNudgeArray[@]}\""
runString="dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength},parentDir=${parentDir},outputDir=${outputDir},nSeed=${nSeed},nRuns=${nRuns},readerDir1=${readerDir1},readerDir2=${readerDir2},startNudgeArray=\"${startNudgeArray[@]}\""

# Look for LAST log of the multi-run parallel slurm job
logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})_$(printf %03d ${startNudgeArray[${#startNudgeArray[@]}-1]})"

#echo 
#echo "$logString"


job_num_pre=$(sbatch --export="ALL,${runString}" a_run_opendrift.sh)

#job_num_split=($job_num_pre)
#jobId=${job_num_split[-1]}

#while [ ! -f z_output/log_${logString}.txt ]; do
while [ ! -f z_output/z_logs/log_${logString}.txt ]; do
    #sleep 300 # The production sleep value here should relate to the sum of delays imposed on the starts of the parallel runs (see the the "run" script)
    sleep 20
done

mv slurm-*.out s_slurm_output/ 2>/dev/null; true


