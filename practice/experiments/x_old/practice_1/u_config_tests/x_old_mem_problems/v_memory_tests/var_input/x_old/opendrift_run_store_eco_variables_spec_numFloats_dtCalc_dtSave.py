# Make input dynamic, for gods' sake

# Upon investigating, memory use depends on the geographical spread of a cloud of points.  Opendrift only reads nearby (geographically) data for
# the timesteps before and after the current timestep, regardless of how many particles are in the cloud.  So, hypothetically, a tight cloud 
# could have millions of points but still not overflow the node memory.  
# Furthermore, the "next timestep" data for the previous timestep becomes the "previous timestep" data for the current timestep.  So, I'm 
# Wondering if we can get away with running 2 seedings at once... will this overflow the memory?  Or will the proximity in space AND time
# be used advantageously by opendrift, and, if so, will it allow 2 seedings to run?  

# New format of metadata - we're always seeding bi-daily, so just indicate the window of the run (in days)

number_of_seeds = 1

days_between_seeds = 2

# Test metadata and configuration
#-------------------------------------------------
#n_runs = int(number_of_seeds/n_days_seed)
n_runs = number_of_seeds
#n_days_seed = n_runs
seed_window = number_of_seeds * days_between_seeds


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
from reader_ROMS_native_custom_eco import Reader

# Track how long this takes to run
t_init = time.time()




#number_of_floats = 1
number_of_floats = int(sys.argv[1])
# dt of compute (minutes)
#run_compute = 60
run_compute = int(sys.argv[2])
# dt of save (minutes)
run_save = int(sys.argv[3])

number_of_seeds = 1
# New format of metadata - we're always seeding bi-daily, so just indicate the number of bi-daily seedings we want

run_string = 'floats_{}_saveDT_{}_calcDT_{}'.format(str(number_of_floats),str(run_save),str(run_compute))

# Make dynamic output directories
parent_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/'
#output_dir_local = 'z_output_{}_{}_{}/'.format(number_of_floats,run_compute,run_save)

output_dir = parent_dir + '/z_output/'

#output_dir = parent_dir + output_dir_local
#output_dir_path = os.path.join(parent_dir,output_dir_local)
#os.mkdir(output_dir_path)

#run_string = 'run_{}_of_{}'.format(run_number,n_runs)
print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: {}'.format(run_string),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
#-------------------------------------------------

# -----------------------------------------------------------------------------
# run configuration parameters:

# 3 month run for each float, so... 3 month pld??
#n_months_pld = 3

n_days_test = 10

#run_dt = timedelta(hours=1)
#save_dt = timedelta(hours=1)
save_dt = timedelta(minutes = run_save)
run_dt = timedelta(minutes = run_compute)

# All tests start at Jan 1, 12pm, 1988
base_datetime = datetime.datetime(1988,1,1,12,0,0)
# -----------------------------------------------------------------------------



#--------- Base Directory Paths -----------
base_path = '/home/blaughli/tracking_project/'

history_base = '/data03/fiechter/WC15N_1988-2010/'

# Making the output path relative, for convenience
#output_base = base_path + 'practice/experiments/practice_1/z_output/'
output_base = 'z_output/'

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


#-------- History Files -----------------
his_dir_year_1 = 'Run_1988/'
#his_dir_year_2 = 'Run_1989/'
his_file_wildcard = 'wc15n_avg_*.nc'
his_file_1 = history_base + his_dir_year_1 + his_file_wildcard
#his_file_2 = history_base + his_dir_year_2 + his_file_wildcard

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------



#----------Seed File---------------------
#seed_file_pre = 'seed_uniform_depths_0_20_points_per_profile_11_test1.txt'

#seed_file = seed_base + seed_file_pre

#----------Runtime Data Text File---------------------
runtime_text_file_pre =  'runtime_data_{}.txt'.format(run_string) 
runtime_text_file =  output_dir + runtime_text_file_pre

#----------Output netCDF File---------------------
#tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))


#tracking_output_pre = 'test_output_{}_{}.nc'.format(str(number_of_seeds),run_string)
tracking_output_pre = 'test_output_{}.nc'.format(run_string)

#tracking_output_file = output_base + tracking_output_pre
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


lons = []
lats = []
zs = []
times = []

# We want profiles of floats at each lat/lon starting point.  Space them "depth_step" (5m) apart, from the surface
# down to a set depth min "min_float_depth" (20m) or the bottom depth, whichever is shallower
min_float_depth = 20
depth_step = 5



# Working on making the start and end times of runs dynamic

#start_seed_month_nudge = (run_number - 1) * n_months_seed
#start_seed_time = base_datetime + relativedelta(months = start_seed_month_nudge)

# Now that I'm working with days in the metadata, this will be more complicated - how to account for entering a new month? Oh, I think this actually handles that
#start_seed_day_nudge = (run_number - 1) * n_days_seed
#start_seed_day_nudge = (run_number - 1) * days_between_seeds
start_seed_day_nudge = 0
start_seed_time = base_datetime + relativedelta(days = start_seed_day_nudge)
#end_seed_time = start_seed_time + relativedelta(days = n_days_seed)
end_seed_time = start_seed_time + relativedelta(days = number_of_seeds)

#assert n_days_seed == (end_seed_time - start_seed_time).days, "number of seed days calculation is wrong"

#for run_day in range(0,n_days_seed,2):

for run_day in range(0,1):
    for ii in range(len(points_in_boxes_lon_lat)):
        for jj in range(np.shape(points_in_boxes_lon_lat[ii])[1]):
            bottom_depth = h[points_in_boxes_i_j[ii][0,jj],points_in_boxes_i_j[ii][1,jj]]
            depth_min = np.floor(min(min_float_depth,bottom_depth))
            for kk in range(int(np.floor(depth_min / depth_step)) + 1):
            #for kk in range(1,2):
                zs.append(-kk*depth_step)
                lons.append(points_in_boxes_lon_lat[ii][0,jj])
                lats.append(points_in_boxes_lon_lat[ii][1,jj])
                times.append(datetime.datetime.strptime(str(start_seed_time+datetime.timedelta(days=run_day)), '%Y-%m-%d %H:%M:%S'))
                    
print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: number of floats specified: {}, length of float arrays: {} (should match)'.format(number_of_floats,len(lons)),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)




# Set run length (typically 3 months longer than seeding period, to let all floats reach the end of their (3 month?) pld
start_run_time = start_seed_time
#end_run_time = end_seed_time + relativedelta(months = n_months_pld)
end_run_time = end_seed_time + relativedelta(days = n_days_test)
n_days_run = int((end_run_time - start_run_time).days)
run_length_days = timedelta(days = n_days_run)



o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for debug information


# ------------------------- Adding Readers --------------------------------
t_read_0 = time.time()

r = Reader(his_file_1)
o.add_reader(r)
#r = Reader(his_file_2)
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

o.seed_elements(lon=lons,lat=lats, z=zs, time=times, origin_marker = 0)

t_run_start = time.time()

o.run(duration=run_length_days, time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list)

t_run_end = time.time()
total_runtime = t_run_end-t_run_start
total_execution_time = t_run_end-t_init

summary_string = '{}, number_of_seeds: {}, days_running_per_seed: {}, readerloading (mins): {}, run_time (hrs): {}, execution_time (hrs): {}\n'.format(run_string,str(number_of_seeds),run_length_days.days-1,round(reader_time/60,3),round(total_runtime/3600,3), round(total_execution_time/3600,3))

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

#with open(runtime_text_file,"a") as out_file: 
#    out_file.write('{}, number_of_seeds: {}, days_running_per_seed: {}, readerloading (mins): {}, run_time (hrs): {}, execution_time (hrs): {}\n'.format(run_string,str(number_of_seeds),run_length_days.days-1,round(reader_time/60,3),round(total_runtime/3600,3), round(total_execution_time/3600,3))) 
        








