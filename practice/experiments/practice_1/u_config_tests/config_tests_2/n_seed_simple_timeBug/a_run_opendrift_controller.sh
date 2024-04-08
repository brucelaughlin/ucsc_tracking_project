#!/bin/bash

logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})"

#SBATCH --job-name ${logString}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu


cd $parentDir

python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240408_noEndSpec_limitedTest.py $dtCalc $dtSave $bufferLength $parentDir $nSeed &> z_output/log_${logString}.txt 

