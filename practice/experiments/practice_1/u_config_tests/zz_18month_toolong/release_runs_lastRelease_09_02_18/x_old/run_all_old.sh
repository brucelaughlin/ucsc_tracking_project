#!/usr/bin/env bash
python opendrift_run_store_eco_variables_1_of_2.py &> z_output/log_1.txt &
python opendrift_run_store_eco_variables_2_of_2.py &> z_output/log_2.txt &
