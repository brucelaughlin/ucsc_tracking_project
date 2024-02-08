#!/usr/bin/env python3
# -*- coding: utf-8 -*-




#-------------------------------------------------
#-------------------------------------------------
test_number = 15
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
from opendrift.readers import reader_ROMS_native, reader_netCDF_CF_generic
#from opendrift.models.oceandrift import OceanDrift
import time
import sys 
import os
from pathlib import Path
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/models"))
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/readers"))
#from larvaldispersal import LarvalDispersal

from larvaldispersal_track_new_variables_trim_test_2 import LarvalDispersal

from reader_ROMS_native_custom_2 import Reader

#import reader_ROMS_native_custom_2
#import reader_ROMS_native_custom_rename

# Track how long this takes to run
t_everything_0 = time.time()


#export_variables_list = ['z','sea_water_temperature','sea_water_salinity','NO3']

export_variables_list = ['z','sea_water_temperature','sea_water_salinity','NO3']


#export_variables_list = ['z','temp','salt','NO3']




#--------- Base Directory Paths -----------
history_base = '/data03/fiechter/WC15N_1988-2010/'
#history_base = '/home/blaughli/tracking_project/jerome_history_files/'

seed_base = '/home/blaughli/tracking_project/practice/seed_input_files/z_output/'
        
output_base = '/home/blaughli/tracking_project/practice/experiments/practice_1/z_output/'


#-------- History File -----------------
his_dir_year = 'Run_1988/'
#his_dir_year = 'z_test/'

# There are daily files in each year directory.  So start by practicing with 1
his_file_wildcard = 'wc15n_avg_*.nc'

his_file = history_base + his_dir_year + his_file_wildcard


#----------Seed File---------------------
seed_file_pre = 'box_points_seed_1.txt'

seed_file = seed_base + seed_file_pre

#----------Runtime Data Text File---------------------

runtime_text_file_pre =  'runtime_data.txt' 

runtime_text_file =  output_base + runtime_text_file_pre


#----------Output netCDF File---------------------
tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))

tracking_output_file = output_base + tracking_output_pre

#----------------------------------------
#----------------------------------------



#his_name_piece = his_file_pre.removesuffix(('.nc'))
#seed_name_piece = '_'.join(seed_file_pre.split('_')[3:]).removesuffix('.txt')
#model_out_file = model_output_pre + his_name_piece + '_' + seed_name_piece + '.nc'



# determine number of particles (ie number of lines in seed file)
#with open(seed_file, "rb") as f:
#    num_particles = sum(1 for _ in f)

#lons = np.empty([num_particles])
#lats = np.empty([num_particles])
#zs = np.empty([num_particles])
lons = []
lats = []
zs = []
times = []

# Read seeding configuration data, pupulate variables

#for seed_file in seed_file_list:
with open(seed_file, 'r') as inputfile:
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
#r = reader_ROMS_native.Reader(his_file)
#o.add_reader(r)

# Trying to get NO3 tracking working... following 'https://github.com/OpenDrift/opendrift/discussions/1198'

#r = reader_ROMS_native_custom_rename.Reader(his_file)
#r = reader_ROMS_native_custom_2.Reader(his_file)
r = Reader(his_file)
o.add_reader(r)
#o.add_reader(reader_nitrate, variables=['NO3'])



#reader_nitrate = reader_ROMS_native_custom_1.Reader(his_file)
#o.add_reader(reader_nitrate, variables=['NO3'])



o.set_config('general:coastline_action', 'previous')
# Search for this config parameter in the base model code; it seems we only have
# 3 options (None, which allows things to move through(?) land, previous, which moves
# particles to the previous location, and stranding, which strands them).
# One would assume that the physics generally prevents things from hitting land???
# Or perhaps we lack the resolution in the history file to prescribe non-divergent
# behavior to particles...?


# restrict to 2D motion?  use the following method call:
# o.disable_vertical_motion()


# Shouldn't I also be able to set parameters like swim speed, etc, 
# using the input text file?  And could maybe have switch variables
# at the beginning or end of the file to control for model settings like
# disabling vertical motion, stranding behavior, etc...?


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

#o.run(time_step=3600, outfile=out_file)
#o.run(time_step=3600, outfile = tracking_output_file)

# I think Jerome's data has daily output
#o.run(steps = 120, time_step=timedelta(minutes=60), outfile = tracking_output_file)

# 30 day run, timestep = 1 day
#o.run(steps = 30, time_step=timedelta(hours=24), outfile = tracking_output_file)

#o.run(duration=timedelta(days=30), time_step=3600, time_step_output=3600, outfile = tracking_output_file)
#o.run(duration=timedelta(days=2), time_step=3600, time_step_output=3600, outfile = tracking_output_file)
o.run(duration=timedelta(days=2), time_step=3600, time_step_output=3600, outfile = tracking_output_file, export_variables = export_variables_list)

t_1 = time.time()
total_runtime = t_1-t_run_0
total_execution_time = t_1-t_everything_0


print(o)

print('\n\ntotal execution time: {}\n\n'.format(total_execution_time))
print('\n\ntotal runtime: {}\n\n'.format(total_runtime))


test_number_printable = '{:03.0f}'.format(test_number)

runtime_file = Path(runtime_text_file)
#with open(r'{}'.format(runtime_text_file),"a") as outfile: 
with open(runtime_text_file,"a") as out_file: 
    #out_file.write('runtime: {}, execution: {}\n'.format(total_runtime, total_execution_time))
    out_file.write('test number: {}, runtime: {}, execution: {}\n'.format(test_number_printable,total_runtime, total_execution_time))
    

#o.plot(linecolor='z', fast=True)

#o.plot_property('z')







