# V2: Paul helping with argparse 

# V1:  Now "number_of_seeds" is an input argument 

#n_days_run = 90
particle_lifetime = 150
#particle_lifetime = 90

# Temporal spacing (days) between seeds
days_between_seeds = 2


import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import subprocess
import glob
import pickle
import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import sys 
import os
from pathlib import Path
import argparse
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/models"))
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/readers"))
from larvaldispersal_track_eco_variables import LarvalDispersal
from reader_ROMS_native_custom_eco import Reader



# Track how long this takes to run
t_init = time.time()

# Variables to track
#----------------------------------------
export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
#----------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--configfile", default="config.yaml", type=str)
parser.add_argument("--jobrunnumber", type=int)
args = parser.parse_args()

config_file = args.configfile
job_run_number = args.jobrunnumber

stream = open(config_file,'r')
cd = yaml.safe_load(stream)    # "cd" is short for "config_dictionary"

run_calc = cd["runCalc"]
run_save = cd["runSave"]
buffer_length = cd["bufferLength"]
number_of_seeds = cd["numberOfSeeds"]

his_dir_1 = cd["jobDirList"][job_run_number]

if (cd["dirListTotal"].index(his_dir_1) == len(cd["dirListTotal"])):
    his_dir_2 = his_dir_1
else:
    his_dir_2 = cd["dirListTotal"][cd["dirListTotal"].index(his_dir_1)+1]

start_nudge = cd["startNudgeList"][job_run_number]
output_dir = cd["outputDir"]

stream.close()

print(run_calc)
print(run_save)
print(buffer_length)
print(number_of_seeds)
print(start_nudge)
print(his_dir_1)
print(his_dir_2)
print(output_dir)


