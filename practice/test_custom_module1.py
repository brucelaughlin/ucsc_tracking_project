#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from opendrift.readers import reader_ROMS_native
#from opendrift.models.oceandrift import OceanDrift
import sys 
import os
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/models_opendrift"))
from larvaldispersal import LarvalDispersal

seed_input_file_base = 'seed_input_files'
seed_input_file_name = 'seed_test_1.txt'

seed_input_file = seed_input_file_base + '/' + seed_input_file_name

# determine number of particles (ie number of lines in seed file)
with open(seed_input_file, "rb") as f:
    num_particles = sum(1 for _ in f)

lons = np.empty([num_particles])
lats = np.empty([num_particles])
zs = np.empty([num_particles])
#time = np.emtpy([num_particles,1],np.unicode_)
#time = np.chararray([num_particles,1])
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
        
        
his_file = '/home/blaughli/tracking_project/history_files/wc12_his.nc'

# Do I need this "special" reader for ROMS files???
roms_his_reader = reader_ROMS_native.Reader(his_file)

o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information
o.add_reader(roms_his_reader)


out_file = 'test_module1_output.nc'

o.seed_elements(lon=lons,lat=lats, z=zs, time=times)

#o.run(time_step=3600, outfile=out_file)
o.run(time_step=3600)
#o.run(time_step=3600)

print(o)

o.plot(linecolor='z', fast=True)


