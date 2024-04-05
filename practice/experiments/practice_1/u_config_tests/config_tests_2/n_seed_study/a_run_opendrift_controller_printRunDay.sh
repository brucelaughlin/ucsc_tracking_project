#!/bin/bash

dtCalc=$1
dtSave=$2
bufferLength=$3
parentDir=$4
nSeed=$5


cd $parentDir

python opendrift_run_store_eco_variables_spec_numFloats_dtCalc_dtSave_240403_printRunDay.py $dtCalc $dtSave $bufferLength $parentDir $nSeed & 

