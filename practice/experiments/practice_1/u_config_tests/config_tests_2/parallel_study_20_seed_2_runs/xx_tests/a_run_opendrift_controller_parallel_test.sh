#!/bin/bash

#logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${startNudge})"
logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})"

#SBATCH --job-name ${logString}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu


cd $parentDir

#python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240403_noEndSpec.py $dtCalc $dtSave $bufferLength $parentDir $nSeed &> z_output/log_${logString}.txt 
#python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240409_varStart.py $dtCalc $dtSave $bufferLength $parentDir $nSeed $startNudge &> z_output/log_${logString}.txt 

echo -e "\n" &> z_output/log_${logString}.txt
printf '%s\n' "${startNudgeArray[@]}" &> z_output/log_${logString}.txt


#for ii in ${startNudgeArray[@]}; do

#    printf '%s\n' $ii

#done



