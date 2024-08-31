#!/bin/bash

#SsBbAaTtCcHh --job-name ${logString}
#SBATCH --job-name opendrift
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd $parentDir

# problem with quote in values????  I don't understand why a one-sided double-quote was being passed, but this fixes it
# https://stackoverflow.com/questions/75995781/remove-double-quotes-from-all-fields-in-an-array-in-bash

startNudgeArray=("${startNudgeArray[@]/#\"}") # remove leading quotes
startNudgeArray=("${startNudgeArray[@]/%\"}") # remove trailing quotes

for ii in ${startNudgeArray[@]}; do
    logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})_$(printf %06d ${ii})"
    python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240829_memTest_V1.py $dtCalc $dtSave $bufferLength $outputDir $nSeed $ii ${hisFileArray[@]} &> $outputDir/z_logs/log_${logString}.txt &
    #python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240829_memTest_V1.py $dtCalc $dtSave $bufferLength $outputDir $nSeed $ii "${hisFileArray[@]}" &> $outputDir/z_logs/log_${logString}.txt &
    #python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240413_production.py $dtCalc $dtSave $bufferLength $outputDir $nSeed $ii $readerDir1 $readerDir2 &> $outputDir/z_logs/log_${logString}.txt &
    
    # SLEEP DISABLED FOR SINGLE-PARTICLE TESTS,
    #sleep 600 #Bump this up to 600 - 900 for production

done
wait # I guess I needed this "wait" statement.  Also perhaps my previous placement of the "&" ( ie &> ) was not working for running the function in a loop


