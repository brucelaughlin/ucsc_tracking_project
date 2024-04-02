#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -=-=================================
# Adding i,j coordinates to get h values before setting seed dephts
# -=-=================================



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
from larvaldispersal_track_eco_variables import LarvalDispersal
from reader_ROMS_native_custom_eco import Reader

# Track how long this takes to run
t_everything_0 = time.time()





# -----------------------------------------------------------------------------
# run configuration parameters:

#-------------------------------------------------
test_metadata = '0_20_21_allreader'
#-------------------------------------------------
run_dt = timedelta(hours=1)
save_dt = timedelta(hours=1)

run_ndays = 4
run_length = timedelta(days=run_ndays)
# -----------------------------------------------------------------------------




#----------file paths---------------------
base_path = '/home/blaughli/tracking_project/practice/'
history_base = '/data03/fiechter/WC15N_1988-2010/'

output_base = base_path + 'experiments/config_tests/z_output/'

points_dir = base_path + 'practice/bounding_boxes/determine_points/z_output/'
points_in_boxes_file_in = points_dir + 'points_in_boxes_lon_lat_combined.p'
points_in_boxes_file_in_ij = points_dir + 'points_in_boxes_i_j_combined.p'

runtime_text_file_pre =  'runtime_data.txt' 
runtime_text_file =  output_base + runtime_text_file_pre

tracking_output_pre = 'test_output_{}_.nc'.format(test_metadata)
tracking_output_file = output_base + tracking_output_pre



#----------------------------------------
export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
#----------------------------------------


# Load coordinates of points in all boxes
file = open(points_in_boxes_file_in,'rb')
points_in_boxes = pickle.load(file)
file.close

file = open(points_in_boxes_file_in_ij,'rb')
points_in_boxes_ij = pickle.load(file)
file.close

lons = []
lats = []
zs = []
times = []

#
## Read seeding configuration data, pupulate variables
#
##for seed_file in seed_file_list:
#with open(seed_file, 'r') as inputfile:
#    for line in inputfile:
#        a,b,c,d = line.rstrip('\n').split(', ')
#        lons.append(float(a))
#        lats.append(float(b))
#        zs.append(float(c))
#        times.append(datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
#            
#lons = np.asarray(lons)
#lats = np.asarray(lats)
#zs = np.asarray(zs)
#





o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information


# Want lazy readers for all files added at beginning; only initialized when needed

#-------- History File -----------------
# There are daily files in each year directory.  23 years total (1988 - 2010)

# Ideally, want readers to be lazy.  Do this with attribute is_lazy  ??
end_year = 2010
num_years = 23
year_val = 1988
year_list = []

#for ii in range(num_years):
while year_val <= end_year:
    his_dir_year = 'Run_{}/'.format(year_val)
    his_file_wildcard = 'wc15n_avg_*.nc'
    his_file = history_base + his_dir_year + his_file_wildcard
    r = Reader(his_file)
    r.is_lazy = True
    o.add_reader(r)
    #year_list.append(year_val)
    print('reader {}/{} added'.format(year_val,end_year))
    year_val+=1

#his_dir_year = 'Run_1988/'
#his_dir_year = 'Run_{}/'.format(
#his_file_wildcard = 'wc15n_avg_*.nc'
#his_file = history_base + his_dir_year + his_file_wildcard



#r = Reader(his_file)
#o.add_reader(r)

o.set_config('general:coastline_action', 'previous')


# Shouldn't I also be able to set parameters like swim speed, etc, 
# using the input text file?  And could maybe have switch variables
# at the beginning or end of the file to control for model settings like
# disabling vertical motion, stranding behavior, etc...?


#--------------------------------------------------------------------------
# Options to disable vertical motion:

# Restrict to 2D motion?  Use the following method call:
# o.disable_vertical_motion()

# Flag for vertical turbulent mixing (default is True)
#o.set_config('drift:vertical_mixing', False)
#--------------------------------------------------------------------------

o.seed_elements(lon=lons,lat=lats, z=zs, time=times, origin_marker = 0)

t_run_0 = time.time()

#o.run(duration=timedelta(days=2), time_step=3600, time_step_output=3600, outfile = tracking_output_file, export_variables = export_variables_list)
o.run(duration=run_length, time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list)

t_1 = time.time()
total_runtime = t_1-t_run_0
total_execution_time = t_1-t_everything_0


print(o)

print('\n\ntotal execution time: {}\n\n'.format(total_execution_time))
print('\n\ntotal runtime: {}\n\n'.format(total_runtime))


#test_number_printable = '{:03.0f}'.format(test_number)

with open(runtime_text_file,"a") as out_file: 
    #out_file.write('test number: {}, runtime: {}, execution: {}\n'.format(test_number_printable,total_runtime, total_execution_time))
    #out_file.write('days: {}, test number: {}, runtime: {}, execution: {}\n'.format(run_ndays,test_metadata,total_runtime, total_execution_time))
    out_file.write('days: {}, test metadata: {}, runtime (hrs): {}, execution (hrs): {}\n'.format(run_ndays,test_metadata,round(total_runtime/3600,3), round(total_execution_time/3600,3)))
    

#o.plot(linecolor='z', fast=True)

#o.plot_property('z')







