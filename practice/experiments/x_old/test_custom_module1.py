#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from opendrift.readers import reader_ROMS_native
#from opendrift.models.oceandrift import OceanDrift
import time
import sys 
import os
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/models_opendrift"))
from larvaldispersal import LarvalDispersal



        
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his.nc'
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his_dummy_zeros.nc'
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his_v0_Ks_1e-3.nc'
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his_v0_Ks_linear_1e-2_1e-1.nc'
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his_v0_Ks_1e-4.nc'
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his_v0_Ks_0_base.nc'
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his_v0_Ks_linear_1e-4_1e-1.nc'
#his_file = '/home/blaughli/tracking_project/history_files/wc12_his_v0_Ks_tanh_1e-3_1.nc'
his_file = '/home/blaughli/tracking_project/history_files/wc12_his_v0_Ks_Kt_Kv_0.nc'

#nc_output_file = 'profile_turb_study_1.nc'
#nc_output_file = 'turbulence_study/profile_turb_study_AKs_1e-3_psi_line_slope1.nc'
nc_output_file = 'turbulence_study/profile_turb_study_wc12_his_v0_Ks_Kt_Kv_0.nc_psi_uniform.nc'


seed_input_file_base = 'seed_input_files'
#seed_input_file_name = 'seed_test_1.txt'
#seed_input_file_name = 'seed_turbulence_test1.txt'

#seed_input_file_name = 'seed_turbulence_test_psi_line_slope1.txt'
seed_input_file_name = 'seed_turbulence_test_psi_uniform.txt'
#out_file = 'test_module_1_turb_test_psi_line_slope_1.nc'





seed_input_file = seed_input_file_base + '/' + seed_input_file_name

# determine number of particles (ie number of lines in seed file)
with open(seed_input_file, "rb") as f:
    num_particles = sum(1 for _ in f)

lons = np.empty([num_particles])
lats = np.empty([num_particles])
zs = np.empty([num_particles])
times = []

# Read seeding configuration data, pupulate varialbes
with open(seed_input_file, 'r') as inputfile:
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




o.seed_elements(lon=lons,lat=lats, z=zs, time=times)


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
#o.set_config('drift:vertical_mixing', False)
o.set_config('drift:vertical_mixing', True)


t0 = time.time()

#o.run(time_step=3600, outfile=out_file)
o.run(time_step=3600, outfile = nc_output_file)

t1 = time.time()
total_runtime = t1-t0


print(o)

print('\n\ntotal runtime: {}\n\n'.format(total_runtime))

#o.plot(linecolor='z', fast=True)

#o.plot_property('z')




