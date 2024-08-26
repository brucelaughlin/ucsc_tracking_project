#!/bin/bash

sbatch --export="ALL,numFloats=1,dtCalc=60,dtSave=60" run_all.sh
sbatch --export="ALL,numFloats=1,dtCalc=60,dtSave=1440" run_all.sh
sbatch --export="ALL,numFloats=1,dtCalc=60,dtSave=2880" run_all.sh
