#!/bin/bash

mkdir -p z_output

dtCalc=60

dtSave=60

bufferLength=100 # default, but must be provided in my code

numFloats=9528


./a_callSlurm.sh $dtCalc $dtSave $bufferLength $numFloats &
