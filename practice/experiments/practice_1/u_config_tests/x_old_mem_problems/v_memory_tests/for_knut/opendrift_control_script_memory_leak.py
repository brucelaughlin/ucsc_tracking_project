# Hi Knut, thank you very much for your time and attention.
#
# This is how I'm running Opendrift;  In this test, I'm using Oceandrift as my model, and reader_ROMS_native as my reader.  I noticed memory leaks
# (ie monotonically increasing memory usage, until overflow) when using my own custom model and reader, so I tried the same setup with a stock
# model and reader.  I am still getting the same apparent "memory leak", when I run this script.
#
# Sincerely, Bruce Laughlin, UCSC Physical Oceanogrphy researcher/pure math MS student in Santa Cruz, CA

buffer_length = 100 # default value
#buffer_length = 50
#buffer_length = 10

n_days_test = 10


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
#sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/models"))
#sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/readers"))
#from larvaldispersal_track_eco_variables import LarvalDispersal
#from larvaldispersal_track_eco_variables_test import LarvalDispersal
#from reader_ROMS_native_custom_eco import Reader
from opendrift.readers import reader_ROMS_native
from opendrift.models.oceandrift import OceanDrift


# Note: 9528 is the exact number of floats I have if I use each of my starting lat/lon coordinate pairs, and have 4 floats
# per horizontal location, in a vertical profile from 0 to 15m  depth in increments of 5m

# Note also that the comments below can be changed so that number of floats, run_calc (minutes!), run_save (minutes!), and buffer_length
# can be read as command line arguments when calling this script (in that order).  Note also that run_calc and run_save are later
# converted to seconds.

number_of_floats = 9528 
#number_of_floats = int(sys.argv[1])
run_calc = 60 # minutes
#run_calc = int(sys.argv[2])
run_save = 60 # minutes
#run_save = int(sys.argv[3])
#buffer_length = int(sys.argv[4])

save_dt = run_save * 60;
run_dt = run_calc * 60

# All tests start at Jan 1, 12pm, 1988
base_datetime = datetime.datetime(1988,1,1,12,0,0)

box_lon_lat_file = 'points_in_boxes_lon_lat_combined.p'

# HUGE ISSUE:  Still haven't resolved how to lazily add readers for all of the files.  
# For this test, we stay in a single year, so we should be ok, but may be a problem
# for the full-scale experiment.
his_file_wildcard = 'wc15n_avg_*.nc'
his_file_1 = his_file_wildcard

#his_file_list = []
#for filename in glob.glob(history_base + his_dir_year_1 + "wc15n_avg_*.nc"):
#    his_file_list.append(filename)
#his_file_list.sort()

tracking_output_file = 'memory_test_output.nc'

#----------------------------------------
#export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
#----------------------------------------

# We want profiles of floats at each lat/lon starting point.  Space them "depth_step" (5m) apart, from the surface
# down to 15m depth
depth_min = 15
depth_step = 5

start_seed_day_nudge = 0
start_seed_time = base_datetime + relativedelta(days = start_seed_day_nudge)
end_seed_time = start_seed_time + relativedelta(days = 1)

lons = []
lats = []
zs = []
times = []

# Load the lat/lon starting locations of our floats
file = open(box_lon_lat_file,'rb')
points_in_boxes_lon_lat = pickle.load(file)
file.close

# The following loop structure allows for any number of floats to be added to the experiment; they are added "in order" according to 
# the locations specified in ""points_in_boxes_lon_lat" (which contains the lon/lat coordinates of points in my analysis boxes along the coast),
# and if more floats than total points (in horizontal + vertical dimension) are specified, this loop just starts over and adds more floats at already-populated
# locations.  Using profiles with 4 depths per horizontal coordinate (0-15m depth, increments of 5), there are a total of 9528 distinct locations for floats
# (there are 2382 distinct horizontal locations).

float_dex = 0
while float_dex < number_of_floats:
    for run_day in range(0,1):
        for ii in range(len(points_in_boxes_lon_lat)):
            for jj in range(np.shape(points_in_boxes_lon_lat[ii])[1]):
                for kk in range(int(np.floor(depth_min / depth_step)) + 1):
                    if float_dex < number_of_floats:
                        zs.append(-kk*depth_step)
                        lons.append(points_in_boxes_lon_lat[ii][0,jj])
                        lats.append(points_in_boxes_lon_lat[ii][1,jj])
                        #times.append(datetime.datetime.strptime(str(start_seed_time+datetime.timedelta(days=run_day)), '%Y-%m-%d %H:%M:%S'))
                        float_dex += 1
                    else:
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            continue
        break

lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)

start_run_time = start_seed_time
end_run_time = end_seed_time + relativedelta(days = n_days_test - 1)
n_days_run = int((end_run_time - start_run_time).days)
run_length_days = timedelta(days = n_days_run)

o = OceanDrift(loglevel=0)  # Set loglevel to 0 for debug information

o.set_config('general:coastline_action', 'previous')

r = reader_ROMS_native.Reader(his_file_1)
o.add_reader(r)

#o.add_readers_from_list(his_file_list)

#r = Reader(his_file_list)
#o.add_reader(r)

#o.seed_elements(lon=lons,lat=lats, z=zs, time=times)
o.seed_elements(lon=lons,lat=lats, z=zs, time=start_seed_time)

#o.run(duration=run_length_days, time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_buffer_length=buffer_length)
#o.run(outfile = tracking_output_file, export_buffer_length=buffer_length)
o.run(outfile = tracking_output_file)

