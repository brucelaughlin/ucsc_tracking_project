#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/models_opendrift"))
from larvaldispersal import LarvalDispersal


#--------- Base Directory Paths -----------
#history_base = '/data03/fiechter/WC15N_1988-2010/'
history_base = '/home/blaughli/tracking_project/jerome_history_files/'

seed_base = '/home/blaughli/tracking_project/practice/seed_input_files/z_output/'
        
output_base = '/home/blaughli/tracking_project/practice/experiments/practice_1/z_output/'


#-------- History File -----------------
his_dir_year = 'Run_1988/'
#his_dir_year = 'z_test/'

# There are daily files in each year directory.  So start by practicing with 1
#his_file_pre = 'wc15n_avg_0001.nc'
his_file_pre = 'wc15n_avg_year.nc'

his_file = history_base + his_dir_year + his_file_pre


#----------Seed File---------------------
seed_file_pre = 'box_points_seed_1.txt'

seed_file = seed_base + seed_file_pre


#----------Output File---------------------

test_number = 3

#tracking_output_pre = 'test_output_2.nc'
tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))

tracking_output_file = output_base + tracking_output_pre

#----------------------------------------
#----------------------------------------



his_name_piece = his_file_pre.removesuffix(('.nc'))
seed_name_piece = '_'.join(seed_file_pre.split('_')[3:]).removesuffix('.txt')

#model_out_file = model_output_pre + his_name_piece + '_' + seed_name_piece + '.nc'



# determine number of particles (ie number of lines in seed file)
with open(seed_file, "rb") as f:
    num_particles = sum(1 for _ in f)

lons = np.empty([num_particles])
lats = np.empty([num_particles])
zs = np.empty([num_particles])
times = []

# Read seeding configuration data, pupulate variables
with open(seed_file, 'r') as inputfile:
    ii = 0
    for line in inputfile:
        a,b,c,d = line.rstrip('\n').split(', ')
        lons[ii] = float(a)
        lats[ii] = float(b)
        zs[ii] = float(c)
        times.append(datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
        ii+=1
        

# Do I need this "special" reader for ROMS files???
roms_his_reader = reader_ROMS_native.Reader(his_file)

o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information
o.add_reader(roms_his_reader)




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



o.seed_elements(lon=lons,lat=lats, z=zs, time=times)



t0 = time.time()

#o.run(time_step=3600, outfile=out_file)
#o.run(time_step=3600, outfile = tracking_output_file)

# I think Jerome's data has daily output
#o.run(steps = 120, time_step=timedelta(minutes=60), outfile = tracking_output_file)

# 30 day run, timestep = 1 day
o.run(steps = 30, time_step=timedelta(hours=24), outfile = tracking_output_file)

t1 = time.time()
total_runtime = t1-t0


print(o)

print('\n\ntotal runtime: {}\n\n'.format(total_runtime))

o.plot(linecolor='z', fast=True)

#o.plot_property('z')




