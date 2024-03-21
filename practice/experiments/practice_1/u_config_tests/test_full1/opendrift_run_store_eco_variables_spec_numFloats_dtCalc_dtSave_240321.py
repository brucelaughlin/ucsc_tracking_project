
n_days_run = 90

# Can finally increase number of seeds per run again.  But, still worried about that "doubling" spike in memory usage
# at the very end of runs... see what happens

number_of_seeds = 10
#number_of_seeds = 1

days_between_seeds = 2


# Make dynamic output directories
parent_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/'
output_dir = parent_dir + 'z_output/'


# Test metadata and configuration
#-------------------------------------------------
#n_runs = int(number_of_seeds/n_days_seed)
n_runs = number_of_seeds
#n_days_seed = n_runs
seed_window_length = number_of_seeds * days_between_seeds

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
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/models"))
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/readers"))
from larvaldispersal_track_eco_variables import LarvalDispersal
#from larvaldispersal_track_eco_variables_test import LarvalDispersal # don't track eco variables
from reader_ROMS_native_custom_eco import Reader

#from opendrift.readers import reader_ROMS_native
#from opendrift.models.oceandrift import OceanDrift

# Track how long this takes to run
t_init = time.time()




# dt of compute (minutes)
#run_calc = 60
run_calc = int(sys.argv[1])
# dt of save (minutes)
run_save = int(sys.argv[2])
buffer_length = int(sys.argv[3])

year_initial = int(sys.argv[4])
day_initial = int(sys.argv[5])

run_string_test = 'calcDT_{b:03d}_saveDT_{c:04d}_buffer_{d:03d}'.format(b=run_calc,c=run_save,d=buffer_length)

#run_string = 'run_{}_of_{}'.format(run_number,n_runs)
print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
#print('USER PRINT STATEMENT: {}'.format(run_string),flush=True)
print('USER PRINT STATEMENT: {}'.format(run_string_test),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
#-------------------------------------------------

# -----------------------------------------------------------------------------
# run configuration parameters:

#save_dt = timedelta(minutes = run_save)
save_dt = run_save * 60;

#run_dt = timedelta(minutes = run_calc)
run_dt = run_calc * 60

# All tests start at Jan 1, 12pm, 1988
base_datetime = datetime.datetime(1988,1,1,12,0,0)
#base_datetime = datetime.datetime(1988,1,2,12,0,0)
# -----------------------------------------------------------------------------



#--------- Base Directory Paths -----------
base_path = '/home/blaughli/tracking_project/'

history_base = '/data03/fiechter/WC15N_1988-2010/'

# Making the output path relative, for convenience
#output_base = base_path + 'practice/experiments/practice_1/z_output/'
output_base = 'z_output/'

box_base = base_path + 'practice/bounding_boxes/determine_initial_points/z_output/'





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


#-------- History Files -----------------
his_dir_year_1 = 'Run_1988/'
#his_dir_year_2 = 'Run_1989/'
his_file_wildcard = 'wc15n_avg_*.nc'
his_file_1 = history_base + his_dir_year_1 + his_file_wildcard
#his_file_2 = history_base + his_dir_year_2 + his_file_wildcard

#his_file_list = []
#for filename in glob.glob(history_base + his_dir_year_1 + "wc15n_avg_*.nc"):
#    his_file_list.append(filename)
#his_file_list.sort()


#----------Output netCDF File---------------------
tracking_output_pre = 'test_output_{}.nc'.format(run_string_test)

tracking_output_file = output_dir + tracking_output_pre







#----------------------------------------
export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
#----------------------------------------


file = open(box_lon_lat_file,'rb')
points_in_boxes_lon_lat= pickle.load(file)
file.close

file = open(box_i_j_file,'rb')
points_in_boxes_i_j= pickle.load(file)
file.close


# We want profiles of floats at each lat/lon starting point.  Space them "depth_step" (5m) apart, from the surface
# down to a set depth min "min_float_depth" (20m) or the bottom depth, whichever is shallower
min_float_depth = 20
#min_float_depth = 15
depth_step = 5



# Working on making the start and end times of runs dynamic

#start_seed_month_nudge = (run_number - 1) * n_months_seed
#start_seed_time = base_datetime + relativedelta(months = start_seed_month_nudge)

# Now that I'm working with days in the metadata, this will be more complicated - how to account for entering a new month? Oh, I think this actually handles that
#start_seed_day_nudge = (run_number - 1) * n_days_seed
#start_seed_day_nudge = (run_number - 1) * days_between_seeds
#start_seed_day_nudge = 0

#start_seed_time = base_datetime + relativedelta(days = start_seed_day_nudge)
start_seed_time = base_datetime + relativedelta(years = year_initial) + relativedelta(days = day_initial)



#end_seed_time = start_seed_time + relativedelta(days = n_days_seed)
#end_seed_time = start_seed_time + relativedelta(days = number_of_seeds)
end_seed_time = start_seed_time + relativedelta(days = seed_window_length)

#assert n_days_seed == (end_seed_time - start_seed_time).days, "number of seed days calculation is wrong"

#for run_day in range(0,n_days_seed,2):

lons = []
lats = []
zs = []
times = []


#for run_day in range(0,1):
for run_day in range(0,end_seed_time,2):
    for ii in range(len(points_in_boxes_lon_lat)):
        for jj in range(np.shape(points_in_boxes_lon_lat[ii])[1]):
            bottom_depth = h[points_in_boxes_i_j[ii][0,jj],points_in_boxes_i_j[ii][1,jj]]
            depth_min = np.floor(min(min_float_depth,bottom_depth))
            for kk in range(int(np.floor(depth_min / depth_step)) + 1):
                zs.append(-kk*depth_step)
                lons.append(points_in_boxes_lon_lat[ii][0,jj])
                lats.append(points_in_boxes_lon_lat[ii][1,jj])
                times.append(datetime.datetime.strptime(str(start_seed_time+datetime.timedelta(days=run_day)), '%Y-%m-%d %H:%M:%S'))

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
#print('USER PRINT STATEMENT: number of floats specified: {}, length of float arrays: {} (should match)'.format(number_of_floats,len(lons)),flush=True)
print('USER PRINT STATEMENT: number of floats seeded: {} '.format(len(lons)),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)




# Set run length (typically 3 months longer than seeding period, to let all floats reach the end of their (3 month?) pld
start_run_time = start_seed_time
#end_run_time = end_seed_time + relativedelta(months = n_months_pld)
#end_run_time = end_seed_time + relativedelta(days = n_days_test)
#end_run_time = end_seed_time + relativedelta(days = n_days_test - 1)
end_run_time = end_seed_time + relativedelta(days = n_days_run - 1)
#n_days_run = int((end_run_time - start_run_time).days)
run_length_days = timedelta(days = n_days_run)



#o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information
o = LarvalDispersal(loglevel=0)  # Set loglevel to 0 for debug information
#o = OceanDrift(loglevel=0)  # Set loglevel to 0 for debug information


# was my reader initialization the memory bug????????????????????????????????????????????????????????????/
# ------------------------- Adding Readers --------------------------------
t_read_0 = time.time()

r = Reader(his_file_1)
#r = reader_ROMS_native.Reader(his_file_1)
o.add_reader(r)

#o.add_readers_from_list(his_file_list)

#r = Reader(his_file_list)
#o.add_reader(r)

t_read_1 = time.time()
reader_time = t_read_1 - t_read_0

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: Minutes taken to add custom readers for 2 years: {}'.format(round(reader_time)/3600,3),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
#--------------------------------------------------------------------------


o.set_config('general:coastline_action', 'previous')


#--------------------------------------------------------------------------
# Options to disable vertical motion:

# Restrict to 2D motion?  Use the following method call:
# o.disable_vertical_motion()

# Flag for vertical turbulent mixing (default is True)
#o.set_config('drift:vertical_mixing', False)
#--------------------------------------------------------------------------

#o.seed_elements(lon=lons,lat=lats, z=zs, time=times, origin_marker = 0)
#o.seed_elements(lon=lons,lat=lats, z=zs, time=start_seed_time, origin_marker = 0)
o.seed_elements(lon=lons,lat=lats, z=zs, time=start_seed_time)

t_run_start = time.time()

o.run(duration=run_length_days, time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list, export_buffer_length=buffer_length)
#o.run(duration=run_length_days, time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list)
#o.run(duration=run_length_days, time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_buffer_length=buffer_length)
#o.run(outfile = tracking_output_file, export_buffer_length=buffer_length)
#o.run(outfile = tracking_output_file)

#o.run(outfile = tracking_output_file)

t_run_end = time.time()
total_runtime = t_run_end-t_run_start
total_execution_time = t_run_end-t_init

#summary_string = '{}, number_of_seeds: {}, days_running_per_seed: {}, readerloading (mins): {}, run_time (hrs): {}, execution_time (hrs): {}\n'.format(run_string,str(number_of_seeds),run_length_days.days-1,round(reader_time/60,3),round(total_runtime/3600,3), round(total_execution_time/3600,3))
summary_string = '{}, number_of_seeds: {}, days_running_per_seed: {}, readerloading (mins): {}, run_time (hrs): {}, execution_time (hrs): {}\n'.format(run_string_test,str(number_of_seeds),run_length_days.days-1,round(reader_time/60,3),round(total_runtime/3600,3), round(total_execution_time/3600,3))

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
#print(o,flush=True)
print('USER PRINT STATEMENT: ' + str(o),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: \ntotal runtime: {}\n'.format(total_runtime),flush=True)
print('USER PRINT STATEMENT: \ntotal execution time: {}\n'.format(total_execution_time),flush=True)
print('USER PRINT STATEMENT: \nsummary info: {}\n'.format(summary_string),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
print('Finished')

        








