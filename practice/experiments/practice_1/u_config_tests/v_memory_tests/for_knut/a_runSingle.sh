#!/bin/bash

#logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})"
logString="$(printf %06d ${numFloats})_$(printf %02d ${dtCalc})_$(printf %03d ${dtSave})_$(printf %03d ${bufferLength})"

#SBATCH --job-name ${logString}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=blaughli@ucsc.edu

cd /home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/for_knut/

#python opendrift_control_script_memory_leak_varInput.py $dtCalc $dtSave $bufferLength  &> log_${logString}.txt 
#python opendrift_control_script_memory_leak_varInput.py $dtCalc $dtSave $bufferLength $numFloats  &> z_output/log_${logString}.txt 
python opendrift_control_script_memory_leak_varInput_setEnv.py $dtCalc $dtSave $bufferLength $numFloats  &> z_output/log_${logString}.txt 

