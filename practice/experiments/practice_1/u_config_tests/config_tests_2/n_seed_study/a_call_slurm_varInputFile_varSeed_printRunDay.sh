#!/bin/bash

dtCalc=$1
dtSave=$2
bufferLength=$3
#inputFile=$4

nSeed=$4

parentDir=$(pwd)

runString="dtCalc=${dtCalc},dtSave=${dtSave},bufferLength=${bufferLength},parentDir=${parentDir},nSeed=${nSeed}"

#job_num_pre=$(sbatch --export="ALL,${runString}" a_run_opendrift_controller_printRunDay.sh)
#--export="ALL,${runString}" ./a_run_opendrift_controller_printRunDay.sh

#$1 $2 $3 $parentDir $4 ./a_run_opendrift_controller_printRunDay.sh

#--export="ALL,${runString}" a_run_opendrift_controller_printRunDay.sh

#"${runString}" a_run_opendrift_controller_printRunDay.sh

#"ALL,${runString}" a_run_opendrift_controller_printRunDay.sh
#$dtCalc $dtSave $bufferLength $parentDir $nSeed ./a_run_opendrift_controller_printRunDay.sh

#./a_run_opendrift_controller_printRunDay.sh $dtCalc $dtSave $bufferLength $parentDir $nSeed 
./a_run_opendrift_controller_printRunDay.sh $dtCalc $dtSave $bufferLength "$parentDir" $nSeed 

#ARGS=(-a )

#$1 $2 $3 $parentDir $4 ./a_run_opendrift_controller_printRunDay.sh

