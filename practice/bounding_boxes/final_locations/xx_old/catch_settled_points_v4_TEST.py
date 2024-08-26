# v4: With a test on 10 files, wasn't findng many exposures to O2 below 2.2 (which we were looking for).  So, in V4, run the catching and 
# histogram construction on a range of O2 levels

# v3: add exposure calculations
# - Also: getting new boxes from the "modified_islands" directory.  No more "inshore/offshore" files 

# v2: Need to add storage of data needed for other stats (want to calculate settlement time pdf/cdf)
# - time to settle (also do this per release box)

# create seasonal pdfs (djf, etc)

# Error - think I need to use lat/lon, as in version 1 I just used i/j which
# depends on the grid type... ie it's wrong to use i/j from a polygon in psi
# to bound rho points... 

# Note that "status" is 0 when the particle is active, and a large magnitude negative
# number when not.  (strange!)


#---------------------------------------------------------------------
#---------------------------------------------------------------------
# I/O
#---------------------------------------------------------------------
#tracking_output_dir_pre = 'test4_physics_only_AKs_1en5/'
tracking_output_dir_pre = 'drift_150_physics_only_AKs_1en5_v1/'
#---------------------------------------------------------------------
tracking_output_base = "/data01/blaughli/tracking_project_output/"
#tracking_output_base = "/data03/blaughli/tracking_project_output/"
#---------------------------------------------------------------------
#---------------------------------------------------------------------




import datetime
import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as plt_path
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint
from os import listdir
from os.path import isfile, join
import sys

#---------------------------------------------------------------------
#---------------------------------------------------------------------
# PARAMETERS and CONSTANTS

#---------------------------------------------------------------------
# Need to know the number of DAYS of each particle's life (fixed unless I change the 
# the deactivation time in the model code)
# NOTE: I believe that the extra point in time in all files is due to there being data saved at "time 0" - so,
# a '90 day run' with daily output will have 91 timesteps because initial state is saved.
#---------------------------------------------------------------------

#run_length_days = 151
run_length_days = 31
#run_length_days = 61
#run_length_days = 91


# Save the number of days in the drifting window before the settlement window opens
##first_settlement_day = 30
first_settlement_day = 21
#first_settlement_day = 31
#first_settlement_day = 61
#first_settlement_day = 91

# Need to hardcode this for now, previous method of "calculating it" based on the input file doesn't work if we're
# using one input file for different maximum PLDs.
timesteps_per_day = 1


# Opendrift output times are seconds since Jan 1, 1979
base_datetime = datetime.datetime(1970,1,1,0,0,0)



# Looking at Jerome's files:
#    float oxygen(ocean_time,s_rho,eta_rho,xi_rho) ;
#      oxygen:long_name = "time-averaged dissolved oxygen concentration" ;
#      oxygen:units = "millimole_oxygen meter-3" ;

# desired units: mg/L
molarMassO2 = 31.999 # g/mol
conversion_factor = molarMassO2/1000  #worked this out on papre

# Limit below which we care about exposure for O2
#oxygen_limit = 7
#oxygen_limit = 2.2
oxygen_limit_list = [2.2,3.1,4.1,6]
#---------------------------------------------------------------------
#---------------------------------------------------------------------

point_type_field = 'rho'
point_type_line = 'psi'

base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

lon_field = np.array(dset['lon_{}'.format(point_type_field)])
lat_field = np.array(dset['lat_{}'.format(point_type_field)])
lon_line = np.array(dset['lon_{}'.format(point_type_line)])
lat_line = np.array(dset['lat_{}'.format(point_type_line)])

dset.close

bounding_boxes_base = base_path + 'practice/bounding_boxes/create_boxes/'
bounding_boxes_continent_dir = bounding_boxes_base + 'continent/z_output/'
bounding_boxes_islands_dir = bounding_boxes_base + 'modify_islands/z_output/'
#bounding_boxes_islands_dir = bounding_boxes_base + 'aa_islands/z_output/'


tracking_output_dir = tracking_output_base + tracking_output_dir_pre
tracking_output_files = [f for f in listdir(tracking_output_dir) if isfile(join(tracking_output_dir,f))]
tracking_output_files.sort()


save_output_file_name = "pdf_data_output_seasonal_rangeO2_pld_{}_{}_".format(first_settlement_day-1,run_length_days-1) + tracking_output_dir_pre[0:-1] + ".p"
#save_output_file_name = "pdf_data_output_seasonal_rangeO2_v4_" + tracking_output_dir_pre[0:-1] + ".p"

save_output_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'
save_output_file = save_output_directory + save_output_file_name


#---------------------------------------------------------------------
# This step is for setting up the pdf data structure which will be modified with each Opendrift output file.
# Also set up constants used throughout the runtime.

tracking_output_file = tracking_output_dir + tracking_output_files[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')
status_all = dset.variables['status'][:]
dset.close()

# Determine the output frequency, n per day.
# Determine the timestep at which the settlement window opens
trajectory_status = status_all[0,:]
trajectory_mask = trajectory_status == 0
#timesteps_per_day = trajectory_mask.sum()/run_length_days
#if timesteps_per_day%1 != 0: sys.exit('(run timesteps)/(run_length_days) was not an integer!')
settlement_window_start = int(timesteps_per_day * first_settlement_day)

# Determine the total number of timesteps in the settlement window
total_number_timesteps = int(np.sum(trajectory_mask))
timesteps_settlement_window = total_number_timesteps - settlement_window_start




#---------------------------------------------------------------------
#---------------------------------------------------------------------
# Prepare the data structure (2D array) for saving the pdf data

bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

n_boxes = 0
for box_lonlat in boxes_lonlat:
    n_boxes += 1

# This approach was producing the wrong number of boxes... it counted 86 instead of 83... not sure why?
## Weird operation needed here to check dimensions, since I used 2D lists for the boxes...
##n_boxes = np.max([len(boxes_lonlat),len(boxes_lonlat[0])])

num_islands = 8
num_last_blob_island = 4
for island_dex in range(num_last_blob_island,num_islands+1):

        bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}.p'.format(island_dex)

        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close        

        for box_lonlat in boxes_lonlat:
            n_boxes += 1
        #n_boxes += np.max([len(boxes_lonlat),len(boxes_lonlat[0])])

#---------------------------------------------------------------------
# Create lists to store statistics for full run and seasonal subsets
#---------------------------------------------------------------------

# Connectivity (release box number vs settlement box number)
pdf_list_connectivity = []
for ii in range(5):
    pdf_list_connectivity.append(np.zeros((n_boxes,n_boxes)))

# Time after PLD until settlement (saving only release location) (release box number vs settlement time)
pdf_list_settleTime_source = []
for ii in range(5):
    pdf_list_settleTime_source.append(np.zeros((n_boxes,timesteps_settlement_window)))

# Time after PLD until settlement (saving only settlement location) (release box number vs settlement time)
pdf_list_settleTime_dest = []
for ii in range(5):
    pdf_list_settleTime_dest.append(np.zeros((n_boxes,timesteps_settlement_window)))

# Number of days eposed to DO levels below 2.2 (saving only settlement location) (release box number vs exposure time)
# note: Think the time dimension needs to be one bigger than the number of possible timesteps (ie need to include an option for "zero") 
#oxygen_limit_list = [2.2,3.1,4.1,6]
pdf_list_of_lists_O2 = []
for jj in range(len(oxygen_limit_list)):
    pdf_list_exposure_oxygen_source = []
    for ii in range(5):
        pdf_list_exposure_oxygen_source.append(np.zeros((n_boxes,timesteps_settlement_window+1)))
        #pdf_list_exposure_oxygen_source.append(np.zeros((n_boxes,timesteps_settlement_window)))
    pdf_list_of_lists_O2.append(pdf_list_exposure_oxygen_source)

# Histogram of average temperature experienced - just estimating range, since I don't know it without processing
#---------------------
# Make sure these match (0.1 = 1, 0.01 = 2, etc)
T_step = 0.1
n_decimals_round = 1
T_scale_factor = int(1/T_step)
#---------------------
T_min = 0
T_max = 30
n_T_steps = len(np.arange(T_min,T_max+1,T_step))
pdf_list_exposure_T_source = []
pdf_list_exposure_T_dest = []
for ii in range(5):
    pdf_list_exposure_T_source.append(np.zeros((n_boxes,n_T_steps)))
    pdf_list_exposure_T_dest.append(np.zeros((n_boxes,n_T_steps)))


#---------------------------------------------------------------------
#---------------------------------------------------------------------
num_files = len(tracking_output_files)
file_number = 0

#---------------------------------------------------------------------
# Need to have a way to see if I'm doing this right... without double counting errors, etc
tracking_output_file = tracking_output_dir + tracking_output_files[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')
particle_labels = dset.variables['trajectory'][:]
dset.close()
num_particles = len(particle_labels)
counter_array=np.zeros((num_particles,num_files))
#---------------------------------------------------------------------


#---------------------------------------------------------------------
# TESTING ONLY
#---------------------------------------------------------------------
#---------------------------------------------------------------------
settlement_boxes_test_array = np.zeros((num_particles,timesteps_settlement_window))
settlement_times_test_array = np.zeros((num_particles,timesteps_settlement_window))
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------


#---------------------------------------------------------------------
# START THE MAIN LOOP!!!
#---------------------------------------------------------------------

#for tracking_output_file_pre in tracking_output_files:

tracking_output_file_pre = tracking_output_files[155]

#    file_number += 1

###TESTING
#if file_number != 177:
#if file_number != 156:
#    continue


tracking_output_file = tracking_output_dir + tracking_output_file_pre

dset = netCDF4.Dataset(tracking_output_file, 'r')

particle_labels = dset.variables['trajectory'][:]
lon_all = dset.variables['lon'][:]
lat_all = dset.variables['lat'][:]
#z_all = dset.variables['z'][:]
status_all = dset.variables['status'][:]
time = np.array(dset['time'])
# Exposure variables 
oxygen_all = dset.variables['oxygen'][:]
temp_all = dset.variables['sea_water_temperature'][:]

dset.close()

oxygen_all *= conversion_factor


# Prepare the list of possible seed months for the run
run_seed_months_list = []
for t in time:
    run_seed_months_list.append(datetime.datetime.strptime(str(base_datetime+datetime.timedelta(seconds=t)), '%Y-%m-%d %H:%M:%S').month)


# Store the total number of particles
num_particles = len(particle_labels)
  
# Determine the output frequency, n per day.
# Determine the timestep at which the settlement window opens
trajectory_status = status_all[0,:]
trajectory_mask = trajectory_status == 0
#    timesteps_per_day = trajectory_mask.sum()/run_length_days
#    if timesteps_per_day%1 != 0: sys.exit('(run timesteps)/(run_length_days) was not an integer!')
settlement_window_start = int(timesteps_per_day * first_settlement_day)

# Determine the total number of timesteps in the settlement window
total_number_timesteps = int(np.sum(trajectory_mask))
timesteps_settlement_window = total_number_timesteps - settlement_window_start

# Create array to store all trajectory locations of all particles during their settlement window
drift_lons = np.zeros((num_particles,timesteps_settlement_window))
drift_lats = np.zeros((num_particles,timesteps_settlement_window))

drift_oxygen = np.zeros((num_particles,timesteps_settlement_window))
drift_T = np.zeros((num_particles,timesteps_settlement_window))


starting_lons = []
starting_lats = []
seed_months = []

last_particle_number = 11844

###for particle_label in particle_labels:
for particle_id in range(len(particle_labels)):

#particle_id = 0

    #if particle_id % last_particle_number == 0:
    if particle_id != 218560:
        continue

    #---------------------------------------------------------------------
    # indent here

    trajectory_status = status_all[particle_id,:]

    # Store month of first timestep of trajectory (ie seeding/starting month)
    seed_months.append(run_seed_months_list[np.where(trajectory_status == 0)[0][0]])

    trajectory_mask = trajectory_status == 0

       
    # Trim the trajectories to prepare for processing!
    particle_lon = lon_all[particle_id,trajectory_mask]
    particle_lat = lat_all[particle_id,trajectory_mask]
    particle_oxygen = oxygen_all[particle_id,trajectory_mask]
    particle_T = temp_all[particle_id,trajectory_mask]

    # Get the STARTING coordinates of each particle
    starting_lons.append(particle_lon[0]) 
    starting_lats.append(particle_lat[0]) 

    # Now that initial positions are known, cut out the "drifting window" and add what remains as a row
    # in the <drift_lons>, <drift_lats> arrays
    drift_lons[particle_id,:] = particle_lon[settlement_window_start:]
    drift_lats[particle_id,:] = particle_lat[settlement_window_start:]

    drift_oxygen[particle_id,:] = particle_oxygen[settlement_window_start:]
    drift_T[particle_id,:] = particle_T[settlement_window_start:]

