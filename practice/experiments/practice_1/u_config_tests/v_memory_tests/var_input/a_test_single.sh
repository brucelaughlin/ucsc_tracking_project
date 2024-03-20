#!/bin/bash

dtCalc=60

dtSave=60

bufferLength=100 # default, but must be provided in my code

./a_call_slurm_single_allFloats.sh $dtCalc $dtSave $bufferLength &
