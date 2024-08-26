#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Now do the 2 hour-separated runs as 2 separate runs

#-------------------------------------------------
#-------------------------------------------------
test_number = '8_1'
#-------------------------------------------------
#-------------------------------------------------







# Try running from two release times, separated by an hour.
# First run as a single run, then do two runs, compare times 

# Now add depth profiles

# Jerome's daily files have just one time value.  So we are working with daily output, ie a timestep of a day

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
from opendrift.readers import reader_ROMS_native
#from opendrift.models.oceandrift import OceanDrift
import time
import sys 
import os
from pathlib import Path
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/models_opendrift"))
from larvaldispersal import LarvalDispersal

# Track how long this takes to run
t_everything_0 = time.time()


#--------- Base Directory Paths -----------
history_base = '/data03/fiechter/WC15N_1988-2010/'
#history_base = '/home/blaughli/tracking_project/jerome_history_files/'

seed_base = '/home/blaughli/tracking_project/practice/seed_input_files/z_output/'
        
output_base = '/home/blaughli/tracking_project/practice/experiments/practice_1/z_output/'


#-------- History File -----------------
his_dir_year = 'Run_1988/'
#his_dir_year = 'z_test/'

# There are daily files in each year directory.  So start by practicing with 1
#his_file_pre = 'wc15n_avg_0001.nc'
#his_file_pre = 'wc15n_avg_year.nc'
his_file_wildcard = 'wc15n_avg_*.nc'

#his_file = history_base + his_dir_year + his_file_pre
his_file = history_base + his_dir_year + his_file_wildcard


#----------Seed File---------------------
seed_file_pre_1 = 'box_points_seed_2_hours_1.txt'
seed_file_pre_2 = 'box_points_seed_2_hours_2.txt'

seed_file_1 = seed_base + seed_file_pre_1
seed_file_2 = seed_base + seed_file_pre_2

seed_file_list = [seed_file_1, seed_file_2]


#----------Runtime Data Text File---------------------

runtime_text_file_pre =  'runtime_data.txt' 

runtime_text_file =  output_base + runtime_text_file_pre


#----------Output netCDF File---------------------
tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))

tracking_output_file = output_base + tracking_output_pre

#----------------------------------------
#----------------------------------------



lons = []
lats = []
zs = []
times = []

# Read seeding configuration data, pupulate variables

with open(seed_file_1, 'r') as inputfile:
    for line in inputfile:
        a,b,c,d = line.rstrip('\n').split(', ')
        lons.append(float(a))
        lats.append(float(b))
        zs.append(float(c))
        times.append(datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
            
lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)



o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information
#o = LarvalDispersal(loglevel=0)  # Set loglevel to 0 for debug information




# Do I need this "special" reader for ROMS files???
r = reader_ROMS_native.Reader(his_file)
o.add_reader(r)


o.set_config('general:coastline_action', 'previous')

# FLAG FOR VERTICAL TURBULENT MIXING
# from oceandrift model cod:
#if self.get_config('drift:vertical_mixing') is False:
#    logger.debug('Turbulent mixing deactivated')
#     return
o.set_config('drift:vertical_mixing', False)
#o.set_config('drift:vertical_mixing', True)

# Setting mixing to True gave an error:
# AttributeError: 'LarvalDispersal' object has no attribute 'set_fallback_values'



o.seed_elements(lon=lons,lat=lats, z=zs, time=times)



t_run_0 = time.time()


# I think Jerome's data has daily output

o.run(duration=timedelta(days=30), time_step=3600, time_step_output=3600, outfile = tracking_output_file)

t_1 = time.time()
total_runtime = t_1-t_run_0
total_execution_time = t_1-t_everything_0


print(o)



#-------------------------------------------------
#-------------------------------------------------
# Second run (1 hour delay
#-------------------------------------------------
#-------------------------------------------------


#-------------------------------------------------
#-------------------------------------------------
test_number = '8_2'
#-------------------------------------------------
#-------------------------------------------------

#----------Output netCDF File---------------------
tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))

tracking_output_file = output_base + tracking_output_pre
#-------------------------------------------------



lons = []
lats = []
zs = []
times = []

# Read seeding configuration data, pupulate variables

with open(seed_file_2, 'r') as inputfile:
    for line in inputfile:
        a,b,c,d = line.rstrip('\n').split(', ')
        lons.append(float(a))
        lats.append(float(b))
        zs.append(float(c))
        times.append(datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
            
lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)



o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information
#o = LarvalDispersal(loglevel=0)  # Set loglevel to 0 for debug information




# Do I need this "special" reader for ROMS files???
r = reader_ROMS_native.Reader(his_file)
o.add_reader(r)


o.set_config('general:coastline_action', 'previous')

# FLAG FOR VERTICAL TURBULENT MIXING
# from oceandrift model cod:
#if self.get_config('drift:vertical_mixing') is False:
#    logger.debug('Turbulent mixing deactivated')
#     return
o.set_config('drift:vertical_mixing', False)
#o.set_config('drift:vertical_mixing', True)

# Setting mixing to True gave an error:
# AttributeError: 'LarvalDispersal' object has no attribute 'set_fallback_values'



o.seed_elements(lon=lons,lat=lats, z=zs, time=times)



t_run_0 = time.time()


# I think Jerome's data has daily output

o.run(duration=timedelta(days=30), time_step=3600, time_step_output=3600, outfile = tracking_output_file)

t_1 = time.time()
total_runtime = t_1-t_run_0
total_execution_time = t_1-t_everything_0


print(o)













