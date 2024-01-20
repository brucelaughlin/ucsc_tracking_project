# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from opendrift.readers import reader_ROMS_native
from opendrift.models.oceandrift import OceanDrift

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
        #time[ii] = float(d)
        #time[ii] = d
        times.append(datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
        ii+=1
        
        
his_file = 'wc12_his.nc'

# Do I need this "special" reader for ROMS files???
roms_his_reader = reader_ROMS_native.Reader(his_file)

o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information
o.add_reader(roms_his_reader)


out_file = 'test2_output.nc'

o.seed_elements(lon=lons,lat=lats, z=zs, time=times)

o.run(time_step=3600, outfile=out_file)

print(o)

o.plot(linecolor='z', fast=True)


