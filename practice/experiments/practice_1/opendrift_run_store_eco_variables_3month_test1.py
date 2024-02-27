#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import pickle
import netCDF4
import matplotlib.pyplot as plt
import numpy as np
#from datetime import datetime
import datetime
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
t_init = time.time()


# -----------------------------------------------------------------------------
# run configuration parameters:

#-------------------------------------------------
#test_number = 1
test_metadata = '6_month_3_release_test1'
#-------------------------------------------------
#run_ndays = 4 #(days)
n_run_months = 6 #(months)

run_dt = timedelta(hours=1)
save_dt = timedelta(hours=1)

#run_length = timedelta(days=run_ndays)
# -----------------------------------------------------------------------------



#--------- Base Directory Paths -----------
base_path = '/home/blaughli/tracking_project/'

history_base = '/data03/fiechter/WC15N_1988-2010/'

seed_base = base_path + 'practice/seed_input_files/z_output/'
        
output_base = base_path + 'practice/experiments/practice_1/z_output/'

box_base = base_path + 'practice/bounding_boxes/determine_points/z_output/'





grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')
h = np.array(dset['h'])
dset.close



#-------- Box Files -----------------

box_file_lon_lat_pre = 'points_in_boxes_lon_lat_combined.p'
box_file_i_j_pre = 'points_in_boxes_i_j_combined.p'

box_lon_lat_file = box_base + box_file_lon_lat_pre
box_i_j_file = box_base + box_file_i_j_pre



# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# HUGE ISSUE:  Still haven't resolved how to lazily add readers for all of the files.  
# For this test, I'll stay in a single year, so we should be ok.


#-------- History File -----------------
his_dir_year = 'Run_1988/'
his_file_wildcard = 'wc15n_avg_*.nc'
his_file = history_base + his_dir_year + his_file_wildcard

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------



#----------Seed File---------------------
#seed_file_pre = 'seed_uniform_depths_0_20_points_per_profile_11_test1.txt'

#seed_file = seed_base + seed_file_pre

#----------Runtime Data Text File---------------------
runtime_text_file_pre =  'runtime_data.txt' 
runtime_text_file =  output_base + runtime_text_file_pre

#----------Output netCDF File---------------------
#tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))


tracking_output_pre = 'test_output_{}.nc'.format(test_metadata)

tracking_output_file = output_base + tracking_output_pre

#----------------------------------------
export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
#----------------------------------------


file = open(box_lon_lat_file,'rb')
points_in_boxes_lon_lat= pickle.load(file)
file.close

file = open(box_i_j_file,'rb')
points_in_boxes_i_j= pickle.load(file)
file.close


lons = []
lats = []
zs = []
times = []

# We want profiles of floats at each lat/lon starting point.  Space them "depth_step" (5m) apart, from the surface
# down to a set depth min "min_float_depth" (20m) or the bottom depth, whichever is shallower
min_float_depth = 20
depth_step = 5



# Working on making the start and end times of runs dynamic

start_seed_month = 1
end_seed_month = start_seed_month + 2
start_seed_time = datetime.datetime(1988,start_seed_month,1,12,0,0)
end_seed_time = datetime.datetime(1988,end_seed_month,1,12,0,0)

n_days_seed = (end_seed_time - start_seed_time).days

for run_day in range(0,n_days_seed,2):
    for ii in range(len(points_in_boxes_lon_lat)):
        for jj in range(len(points_in_boxes_lon_lat[ii])):
            #bottom_depth = h[points_in_boxes_i_j[ii][jj][0],points_in_boxes_i_j[ii][jj][1]]
            bottom_depth = h[points_in_boxes_i_j[ii][0,jj],points_in_boxes_i_j[ii][1,jj]]
            depth_min = np.floor(min(min_float_depth,bottom_depth))
            for kk in range(int(np.floor(depth_min / depth_step)) + 1):
                zs.append(kk*depth_step)
                lons.append(points_in_boxes_lon_lat[ii][0,jj])
                lats.append(points_in_boxes_lon_lat[ii][1,jj])
                #times.append(str(start_seed_time+datetime.timedelta(days=run_day)))
                times.append(datetime.datetime.strptime(str(start_seed_time+datetime.timedelta(days=run_day)), '%Y-%m-%d %H:%M:%S'))
                    
lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)
#times = np.asarray(times)


# Set run length (typically 3 months longer than seeding period, to let all floats reach the end of their (3 month?) pld
start_run_month = start_seed_month
#end_run_month = start_run_month + n_run_months - 1
end_run_month = start_run_month + n_run_months
start_run_time = datetime.datetime(1988,start_run_month,1,12,0,0)
end_run_time = datetime.datetime(1988,end_run_month,1,12,0,0)
#n_days_run = (end_run_time - start_run_time).days
n_days_run = int((end_run_time - start_run_time).days)
run_length_days = timedelta(days = n_days_run)



o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information

r = Reader(his_file)
o.add_reader(r)

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

t_run_start = time.time()

#o.run(duration=timedelta(days=2), time_step=3600, time_step_output=3600, outfile = tracking_output_file, export_variables = export_variables_list)
o.run(duration=run_length_days, time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list)
#o.run(duration=timedelta(days=run_length_days), time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list)

t_run_end = time.time()
total_runtime = t_run_end-t_run_start
total_execution_time = t_run_end-t_init


print(o)

print('\n\ntotal execution time: {}\n\n'.format(total_execution_time))
print('\n\ntotal runtime: {}\n\n'.format(total_runtime))



with open(runtime_text_file,"a") as out_file: 
    #out_file.write('days: {}, test metadata: {}, runtime (hrs): {}, execution (hrs): {}\n'.format(run_length_days.days,test_metadata,round(total_runtime/3600,3), round(total_execution_time/3600,3)))    
    out_file.write('days: {}, run_dt (seconds): {}, save_dt (seconds): {}, test metadata: {}, runtime (hrs): {}, execution (hrs): {}, start_time_init: {}, start_time_run: {}, end_time: {}\n'.format(run_length_days.days,run_dt.seconds,save_dt.seconds,test_metadata,round(total_runtime/3600,3), round(total_execution_time/3600,3)),t_init,t_run_start,t_run_end)    

#o.plot(linecolor='z', fast=True)

#o.plot_property('z')







