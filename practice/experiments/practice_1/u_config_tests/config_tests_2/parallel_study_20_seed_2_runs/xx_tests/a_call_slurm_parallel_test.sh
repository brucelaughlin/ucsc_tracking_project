#!/bin/bash

dtCalc=$1
dtSave=$2
bufferLength=$3
nSeed=$4
# From https://stackoverflow.com/questions/17219453/bash-command-line-arguments-into-an-array-and-subset-the-array-based-on-the-para
# Notice the 5 below... that should be the number after the last parameter number above (currently 4, from nSeed=$4)
startNudgeArray=("${@:5:$1}")

nRuns=${#startNudgeArray[@]}

#echo -e "\n"
#echo $nRuns

#echo -e "\n"
#printf '%s\n' "${startNudgeArray[@]}"



parentDir=$(pwd)

runString="dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength},parentDir=${parentDir},nSeed=${nSeed},startNudgeArray=\"${startNudgeArray[@]}\",nRuns=${nRuns}"
logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})"

job_num_pre=$(sbatch --export="ALL,${runString}" a_run_opendrift_controller_parallel_test.sh)

#echo -e "\n"
#echo $runString
#echo -e "\n"
#echo $logString

