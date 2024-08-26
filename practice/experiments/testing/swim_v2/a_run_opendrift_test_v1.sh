#!/bin/bash

#SsBbAaTtCcHh --job-name ${logString}
#SBATCH --job-name opendrift
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

echo "hi3"

cd $parentDir

# problem with quote in values????  I don't understand why a one-sided double-quote was being passed, but this fixes it
# https://stackoverflow.com/questions/75995781/remove-double-quotes-from-all-fields-in-an-array-in-bash

logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})_$(printf %06d 0)"
python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240729_production_test_v2.py $dtCalc $dtSave $bufferLength $outputDir $nSeed $ii $readerDir1 $readerDir2 &> $outputDir/z_logs/log_${logString}.txt &
#python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240729_production_test_v1.py $dtCalc $dtSave $bufferLength $outputDir $nSeed $ii $readerDir1 $readerDir2 &> $outputDir/z_logs/log_${logString}.txt &
    

wait # I guess I needed this "wait" statement.  Also perhaps my previous placement of the "&" ( ie &> ) was not working for running the function in a loop


