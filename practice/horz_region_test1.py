# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:48:08 2023

@author: blaug
"""

import matplotlib.pyplot as plt
import numpy as np
from opendrift.readers import reader_ROMS_native
from opendrift.models.oceandrift import OceanDrift

from netCDF4 import Dataset

his_file = 'wc12_his.nc'

# Do I need this "special" reader for ROMS files???
roms_his_reader = reader_ROMS_native.Reader(his_file)

his_data = Dataset(his_file)

# 50-60, 100-120

rho_lon = np.array(his_data.variables['lon_rho'][:])
rho_lat = np.array(his_data.variables['lat_rho'][:])

lon_pre = rho_lon[50:53,100:103]
lat_pre = rho_lat[50:53,100:103]

lon_pre = lon_pre.flatten()
lat_pre = lat_pre.flatten()

num_rho = lon_pre.size

# this is rough - here i'm just choosing an arbitrary number of
# depth levels, to be used for all rho points
num_depths = 3

lon_use = np.repeat(lon_pre,num_depths)
lat_use = np.repeat(lat_pre,num_depths)



# how to get depths at rho points?  should be uniquely specifying depth 
# distributions at each rho point

z_single=np.linspace(0, -150, num_depths)

z_use = np.tile(z_single,num_rho)


# need to know model timestep.  should we release every timestep?
# every hour?

#timesteps_release = 10

#num_points = z.size * timesteps_release

num_points = z_use.size
time_start=roms_his_reader.start_time


o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information
o.add_reader(roms_his_reader)



#o.seed_elements(lon_use,lat_use, radius=0, number=, z=np.linspace(0, -150, 10), time=roms_his_reader.start_time)
o.seed_elements(lon_use,lat_use, radius=0, z=z_use, time=roms_his_reader.start_time)


o.run(time_step=3600)

print(o)

o.plot(linecolor='z', fast=True)











