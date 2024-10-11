#v2: reader has a way to specify new variables, so don't need custom reader!

#particle_lifetime = 10
#particle_lifetime = 150

# Temporal spacing (days) between seeds
#days_between_seeds = 2


import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import subprocess
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
import argparse
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/models"))
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/readers"))
from reader_ROMS_native_h5netcdf_mod import Reader


# Track how long this takes to run
t_init = time.time()

# Variables to track
#----------------------------------------
export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
#----------------------------------------

# Variables we'll add to the reader, which aren't defined in reader file
new_variables = {
    'CO2flx': 'CO2flx',
    'CalC': 'CalC',
    'DON': 'DON',
    'NH4': 'NH4',
    'NO3': 'NO3',
    'PON': 'PON',
    'Pzooplankton': 'Pzooplankton',
    'SiOH4': 'SiOH4',
    'TIC': 'TIC',
    'alkalinity': 'alkalinity',
    'diatom': 'diatom',
    'mesozooplankton': 'mesozooplankton',
    'microzooplankton': 'microzooplankton',
    'nanophytoplankton': 'nanophytoplankton',
    'omega': 'omega',
    'opal': 'opal',
    'oxygen': 'oxygen',
    'pCO2': 'pCO2',
    'pH': 'pH',
    }

parser = argparse.ArgumentParser()
parser.add_argument("--configfile", default="config.yaml", type=str)
parser.add_argument("--jobrunnumber", type=int)
args = parser.parse_args()

config_file = args.configfile
job_run_number = args.jobrunnumber

stream = open(config_file,'r')
config_dict = yaml.safe_load(stream)    

# Import the correct Opendrift model
behavior = config_dict["behavior"]
if behavior == "physicsOnly": 
    model_file = "larvaldispersal_track_eco_variables"
    from larvaldispersal_track_eco_variables import LarvalDispersal
elif behavior == "dvm":
    model_file =  "larvaldispersal_track_eco_variables_dielMigration"
    from larvaldispersal_track_eco_variables_dielMigration import LarvalDispersal



print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: Model file: {}'.format(model_file),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

run_calc = config_dict["runCalc"]
run_save = config_dict["runSave"]
buffer_length = config_dict["bufferLength"]
number_of_seeds = config_dict["numberOfSeeds"]
days_between_seeds = config_dict["seedSpacing"]
particle_lifetime = config_dict["particleLifetime"]


his_dir_1 = config_dict["jobDirList"][job_run_number]

if (config_dict["dirListTotal"].index(his_dir_1) == len(config_dict["dirListTotal"])):
    his_dir_2 = his_dir_1
else:
    his_dir_2 = config_dict["dirListTotal"][config_dict["dirListTotal"].index(his_dir_1)+1]

start_nudge = config_dict["startNudgeList"][job_run_number]
output_dir = config_dict["outputDir"]

stream.close()

run_string = 'calcDT_{b:03d}_saveDT_{c:04d}_buffer_{d:03d}_nSeed_{e:03d}_startNudge_{f:06d}'.format(b=run_calc,c=run_save,d=buffer_length,e=number_of_seeds,f=start_nudge)

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: {}'.format(run_string),flush=True)
#print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
#print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
#print('USER PRINT STATEMENT: ',flush=True)
#print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
print('USER PRINT STATEMENT: his_dir_1: {}'.format(his_dir_1),flush=True)
print('USER PRINT STATEMENT: his_dir_2: {}'.format(his_dir_2),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
#-------------------------------------------------


# -----------------------------------------------------------------------------
# run configuration parameters:
#output_dir = parent_dir + '/z_output/'
output_dir = output_dir + '/'
seed_window_length = (number_of_seeds - 1) * days_between_seeds + 1
save_dt = run_save * 60;
run_dt = run_calc * 60

# CHANGE BASE TIME DEPENDING ON WHETHER YOU'RE USING THE 1988-2010 FILES OR THE 1990-2100 FILES 
#base_datetime = datetime.datetime(1990,1,1,12,0,0)
base_datetime = datetime.datetime(1988,1,1,12,0,0)
# -----------------------------------------------------------------------------



#--------- Base Directory Path -----------
base_path = '/home/blaughli/tracking_project/'

# -------- Grid File -----------
grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')
h = np.array(dset['h'])
dset.close

#-------- Box Files -----------------
box_base = base_path + 'practice/bounding_boxes/determine_initial_points/z_output/'
box_file_lon_lat_pre = 'points_in_boxes_lon_lat_combined.p'
box_file_i_j_pre = 'points_in_boxes_i_j_combined.p'
box_lon_lat_file = box_base + box_file_lon_lat_pre
box_i_j_file = box_base + box_file_i_j_pre


#-------- History Files -----------------
his_file_wildcard = 'wc15n_avg_*.nc'
his_file_1 = his_dir_1 + '/' + his_file_wildcard
his_file_2 = his_dir_2 + '/' + his_file_wildcard
#his_file_1 = his_dir_1 + his_file_wildcard
#his_file_2 = his_dir_2 + his_file_wildcard


#----------Output netCDF File---------------------
tracking_output_pre = 'tracking_output_{}.nc'.format(run_string)
tracking_output_file = output_dir + tracking_output_pre

# prepare memory plot file name
output_file_split = tracking_output_file.split('.')
output_file_pre = output_file_split[0]
output_png_file = output_file_pre + '.png'


#--------- Get box data ------------
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


# Compute the seeding time window
start_seed_time = base_datetime + relativedelta(days = start_nudge)
end_seed_time = start_seed_time + relativedelta(days = seed_window_length)


# Prepare lists of coordinates for seeding
lons = []
lats = []
zs = []
times = []



for run_day in range(0,seed_window_length,days_between_seeds): 
    for ii in range(len(points_in_boxes_lon_lat)):
        for jj in range(np.shape(points_in_boxes_lon_lat[ii])[1]):
            bottom_depth = h[points_in_boxes_i_j[ii][0,jj],points_in_boxes_i_j[ii][1,jj]]
            depth_min = np.floor(min(min_float_depth,bottom_depth))
            for kk in range(int(np.floor(depth_min / depth_step)) + 1):
                zs.append(-kk*depth_step)
                lons.append(points_in_boxes_lon_lat[ii][0,jj])
                lats.append(points_in_boxes_lon_lat[ii][1,jj])
                times.append(datetime.datetime.strptime(str(start_seed_time+datetime.timedelta(days=run_day)), '%Y-%m-%d %H:%M:%S'))



# Test, make sure things work.  Just run one particle per run.
#for run_day in range(1):
#    for ii in range(1):
#        for jj in range(1):
#            bottom_depth = h[points_in_boxes_i_j[ii][0,jj],points_in_boxes_i_j[ii][1,jj]]
#            depth_min = np.floor(min(min_float_depth,bottom_depth))
#            for kk in range(1):
#                zs.append(-kk*depth_step)
#                lons.append(points_in_boxes_lon_lat[ii][0,jj])
#                lats.append(points_in_boxes_lon_lat[ii][1,jj])
#                times.append(datetime.datetime.strptime(str(start_seed_time+datetime.timedelta(days=run_day)), '%Y-%m-%d %H:%M:%S'))



print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: number of floats seeded: {} '.format(len(lons)),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

lons = np.asarray(lons)
lats = np.asarray(lats)
zs = np.asarray(zs)


# Calculate run duration in hours
duration_safety_buffer = 3
run_duration_hours = (seed_window_length + particle_lifetime + duration_safety_buffer) * 24

# ------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------
# Initialize Opendrift
o = LarvalDispersal(loglevel=20)  # Set loglevel to 0 for full debug information, 50 for no output
#o = LarvalDispersal(loglevel=0)  # For Testing

# ------------------------- Adding Reader --------------------------------
t_read_0 = time.time()

r = Reader(his_file_1, standard_name_mapping=new_variables)
#r = ReaderEco(his_file_1)
o.add_reader(r)

if his_dir_1 != his_dir_2:
    r = Reader(his_file_2, standard_name_mapping=new_variables)
    #r = ReaderEco(his_file_2)
    o.add_reader(r)

t_read_1 = time.time()
reader_time = t_read_1 - t_read_0





print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: Minutes taken to add custom readers for 2 years: {}'.format(round(reader_time)/3600,3),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
#--------------------------------------------------------------------------


#o.set_config('general:coastline_action', 'previous')


#--------------------------------------------------------------------------
# Options to disable vertical motion:

# Restrict to 2D motion?  Use the following method call:
# o.disable_vertical_motion()

# Flag for vertical turbulent mixing (default is True)
#o.set_config('drift:vertical_mixing', False)
#--------------------------------------------------------------------------

o.seed_elements(lon=lons,lat=lats, z=zs, time=times, origin_marker = 0)

t_run_start = time.time()

#o.run(time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list, export_buffer_length=buffer_length)
o.run(duration=timedelta(hours=run_duration_hours), time_step=run_dt, time_step_output=save_dt, outfile = tracking_output_file, export_variables = export_variables_list, export_buffer_length=buffer_length)

# plot memory usage, safe figure
#o.plot_memory_usage(filename=output_png_file)

t_run_end = time.time()
total_runtime = t_run_end-t_run_start
total_execution_time = t_run_end-t_init

summary_string = '{}, time_start: {}, time_end: {},  number_of_seeds: {}, days_particle_lifetime: {}, readerloading (mins): {}, run_time (hrs): {}, execution_time (hrs): {}\n'.format(run_string,str(t_init),str(t_run_end),str(number_of_seeds),particle_lifetime,round(reader_time/60,3),round(total_runtime/3600,3), round(total_execution_time/3600,3))

print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: ' + str(o),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)
print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: \nprogram start time: {}\n'.format(t_init),flush=True)
print('USER PRINT STATEMENT: \nopendrift start time: {}\n'.format(t_init),flush=True)
print('USER PRINT STATEMENT: \nend time: {}\n'.format(t_run_end),flush=True)
#print('USER PRINT STATEMENT: \ntotal runtime: {} hours\n'.format(round(total_runtime/3600,1)),flush=True)
#print('USER PRINT STATEMENT: \ntotal execution time: {} hours\n'.format(round(total_execution_time/3600,1)),flush=True)
print('USER PRINT STATEMENT: \ntotal runtime: {} hours\n'.format(round(total_runtime/3600,4)),flush=True)
print('USER PRINT STATEMENT: \ntotal execution time: {} hours\n'.format(round(total_execution_time/3600,4)),flush=True)
print('USER PRINT STATEMENT: \nsummary info: {}\n'.format(summary_string),flush=True)
#print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)

        

# Compress the output file

bash_command = "ls -lh {}".format(tracking_output_file)
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
size_raw = process.stdout.read()


bash_command = "nc_compress {}".format(tracking_output_file)
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

time.sleep(120)

bash_command = "ls -lh {}".format(tracking_output_file)
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
size_compressed = process.stdout.read()

#print('USER PRINT STATEMENT: vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',flush=True)
print('USER PRINT STATEMENT: \noutput file size (raw): {}\n'.format(size_raw),flush=True)
print('USER PRINT STATEMENT: \noutput file size (compressed): {}\n'.format(size_compressed),flush=True)
print('USER PRINT STATEMENT: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',flush=True)


print('Finished',flush=True)





