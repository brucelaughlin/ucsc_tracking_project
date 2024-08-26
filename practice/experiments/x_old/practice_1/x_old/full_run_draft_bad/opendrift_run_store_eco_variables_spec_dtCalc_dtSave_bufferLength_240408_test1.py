

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
from reader_ROMS_native_custom_eco import Reader

# Track how long this takes to run
t_init = time.time()

# Temporal spacing (days) between seeds
days_between_seeds = 2

run_calc = int(sys.argv[1])
run_save = int(sys.argv[2])
buffer_length = int(sys.argv[3])

# Make dynamic output directories
output_dir = sys.argv[4]

year_nudge = int(sys.argv[5])
month_nudge = int(sys.argv[6])
final_year_flag = int(sys.argv[7])

#number_of_seeds = int(sys.argv[5])
number_of_seeds = 180

# Need to stop the last seeding window 90 days before we run out of data
if final_year_flag:
    number_of_seeds = 137 #Assuming bi-daily seeding, seed only single year, and prevent 90-day runs going beyond end of year

run_string = 'calcDT_{b:03d}_saveDT_{c:04d}_buffer_{d:03d}_nSeed_{e:02d}'.format(b=run_calc,c=run_save,d=buffer_length,e=number_of_seeds)

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: {}'.format(run_string),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

# -----------------------------------------------------------------------------
# run configuration parameters:
save_dt = run_save * 60;

run_dt = run_calc * 60

seed_window_length = (number_of_seeds - 1) * days_between_seeds + 1
base_datetime = datetime.datetime(1988,1,1,12,0,0)
start_seed_time = base_datetime + relativedelta(years = year_nudge) + relativedelta(months = month_nudge)
end_seed_time = start_seed_time + relativedelta(days = seed_window_length)
base_year = 1988
# -----------------------------------------------------------------------------



#--------- Base Directory Paths -----------
base_path = '/home/blaughli/tracking_project/'

history_base = '/data03/fiechter/WC15N_1988-2010/'

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

#-------- History Files -----------------
his_dir_year_1 = 'Run_' + str(base_year + year_nudge) + '/'
his_dir_year_2 = 'Run_' + str(baes_year + year_nudge + 1) + '/'
his_file_wildcard = 'wc15n_avg_*.nc'
his_file_1 = history_base + his_dir_year_1 + his_file_wildcard
his_file_2 = history_base + his_dir_year_2 + his_file_wildcard

#----------Output netCDF File---------------------
tracking_output_pre = 'run_output_{}.nc'.format(run_string)
tracking_output_file = output_dir + tracking_output_pre

#----------------------------------------
export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
#----------------------------------------

# Load the initial seeding location data
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

# Prepare the seeding lists (we're not using an external file, this is simpler for my wee brain)
lons = []
lats = []
zs = []
times = []

for run_day in range(0,seed_window_length,days_between_seeds): 
    #for ii in range(len(points_in_boxes_lon_lat)):
    for ii in range(40,41):
        #for jj in range(np.shape(points_in_boxes_lon_lat[ii])[1]):
        for jj in range(1):
            bottom_depth = h[points_in_boxes_i_j[ii][0,jj],points_in_boxes_i_j[ii][1,jj]]
            depth_min = np.floor(min(min_float_depth,bottom_depth))
            #for kk in range(int(np.floor(depth_min / depth_step)) + 1):
            for kk in range(1):
                zs.append(-kk*depth_step)
                lons.append(points_in_boxes_lon_lat[ii][0,jj])
                lats.append(points_in_boxes_lon_lat[ii][1,jj])
                times.append(datetime.datetime.strptime(str(start_seed_time+datetime.timedelta(days=run_day)), '%Y-%m-%d %H:%M:%S'))

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: number of floats seeded: {} '.format(len(lons)),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)

# Initialize the model
o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for full debug information, 50 for no output
#o = LarvalDispersal(loglevel=0)  # Set loglevel to 0 for debug information

# Seed the floats
o.seed_elements(lon=lons,lat=lats, z=zs, time=times, origin_marker = 0)


# ------------------------- Adding Readers --------------------------------
t_read_0 = time.time()

r = Reader(his_file_1)
o.add_reader(r)

# Add second year reader if not in final year
if ~final_year_flag:
    r = Reader(his_file_2)
    o.add_reader(r)

t_read_1 = time.time()
reader_time = t_read_1 - t_read_0

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: Minutes taken to add custom readers for 2 years: {}'.format(round(reader_time)/3600,3),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
#--------------------------------------------------------------------------

# Set particles to reflect (rather than settle) off of the coastline.  Should probably set this in the model code, not here
o.set_config('general:coastline_action', 'previous')

#--------------------------------------------------------------------------
# Options to disable vertical motion:
#--------------------------------------------------------------------------
# Restrict to 2D motion?  Use the following method call:
# o.disable_vertical_motion()

# Flag for vertical turbulent mixing (default is True)
#o.set_config('drift:vertical_mixing', False)
#--------------------------------------------------------------------------

t_run_start = time.time()

o.run(time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list, export_buffer_length=buffer_length)

t_run_end = time.time()
total_runtime = t_run_end-t_run_start
total_execution_time = t_run_end-t_init

summary_string = '{}, number_of_seeds: {}, readerloading (mins): {}, run_time (hrs): {}, execution_time (hrs): {}\n'.format(run_string,str(number_of_seeds),round(reader_time/60,3),round(total_runtime/3600,3), round(total_execution_time/3600,3))

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: ' + str(o),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: \ntotal runtime: {}\n'.format(total_runtime),flush=True)
print('USER PRINT STATEMENT: \ntotal execution time: {}\n'.format(total_execution_time),flush=True)
print('USER PRINT STATEMENT: \nsummary info: {}\n'.format(summary_string),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
print('Finished')



bash_command_compress = "nc_compress {}".format(tracking_output_file)
process = subprocess.Popen(bash_command_compress.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
