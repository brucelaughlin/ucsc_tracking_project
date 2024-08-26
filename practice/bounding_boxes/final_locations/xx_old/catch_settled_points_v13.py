#---------------------------------------------------------------------
#---------------------------------------------------------------------
# Define the PLD for the species listed in Mallarie Yeager's report
#---------------------------------------------------------------------

## KELP BASS
first_settlement_day = 20
last_settlement_day = 29
##last_settlement_day = 30

## CALIFORNIA SHEEPHEAD
#first_settlement_day = 30
#last_settlement_day = 59
##last_settlement_day = 60

## KELP ROCKFISH
#first_settlement_day = 60
#last_settlement_day = 89
##last_settlement_day = 90

## BLUE ROCKFISH, BLACK ROCKFISH
#first_settlement_day = 90
#last_settlement_day = 149
##last_settlement_day = 150

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# v13: I confused myself in the last version.  So, now convert to np arrays instead of "lists of lists", and hope that the logic becomes clearer

# v12: Why am I ignoring the 0th timestep (the initial condition)?  Let's try keeping that.  So make the number of timesteps in the run one greater.

# v11: I'VE BEEN CALCULATING EXPOSURE INCORRECTLY - I'm sure that we want exposure data for the ENTIRE lifetime of the larvae, no just during the PLD!
#       So, need to fix the "drift_lons", etc, logic

# create seasonal pdfs (djf, etc)

# Note that "status" is 0 when the particle is active, and a large magnitude negative
# number when not.  (strange!)


#---------------------------------------------------------------------
#---------------------------------------------------------------------
# I/O
#---------------------------------------------------------------------
tracking_output_dir_pre = 'z_two_file_test/'
#tracking_output_dir_pre = 'z_ten_file_test/'
#tracking_output_dir_pre = 'test4_physics_only_AKs_1en5/'
#tracking_output_dir_pre = 'drift_150_physics_only_AKs_1en5_v1/'
#---------------------------------------------------------------------
#tracking_output_base = "/data01/blaughli/tracking_project_output/"
tracking_output_base = "/data03/blaughli/tracking_project_output/"
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
#import scipy.stats as stats


#---------------------------------------------------------------------
#---------------------------------------------------------------------
# PARAMETERS and CONSTANTS


#---------------------------------------------------------------------
# Need to know the number of DAYS of each particle's life (fixed unless I change the 
# the deactivation time in the model code)
# NOTE: I believe that the extra point in time in all files is due to there being data saved at "time 0" - so,
# a '90 day run' with daily output will have 91 timesteps because initial state is saved.
#---------------------------------------------------------------------


# THIS is the v5 adjustment: need to only use data from the pld, which begins after "first_settlement_day" and ends after "last_settlement_day"
#pld_length_days = last_settlement_day - first_settlement_day - 1
#pld_length_days = last_settlement_day - first_settlement_day
pld_length_days = last_settlement_day - first_settlement_day + 1


# Create truncated normal distribution to draw from for settlement window openings
# Data taken from the report provided by Will (page 33, assuming mean is in the middle of PLD ranges, assuming ranges represent 3 stardard deviations)
#mu, sigma, lower, upper  = 120, 10, 90, 150


##---------------------------------------------------------------------
## Bio window distribution - no longer using this
##---------------------------------------------------------------------
#lower = 0
##lower = first_settlement_day
#upper = last_settlement_day - first_settlement_day
##upper = last_settlement_day
#number_standard_deviations = 2
##number_standard_deviations = 3
#
#mu = (upper-lower)/2
#sigma = (upper - mu)/number_standard_deviations
#biological_window_truncNorm_distribution = stats.truncnorm(-number_standard_deviations, number_standard_deviations, loc=mu, scale=sigma)
##---------------------------------------------------------------------


# Need to hardcode this for now, previous method of "calculating it" based on the input file doesn't work if we're
# using one input file for different maximum PLDs.
timesteps_per_day = 1


# Opendrift output times are seconds since Jan 1, 1979
base_datetime = datetime.datetime(1970,1,1,0,0,0)



# Looking at Jerome's files:
#    float O2(ocean_time,s_rho,eta_rho,xi_rho) ;
#      O2:long_name = "time-averaged dissolved O2 concentration" ;
#      O2:units = "millimole_O2 meter-3" ;

# desired units: mg/L
molarMassO2 = 31.999 # g/mol
conversion_factor = molarMassO2/1000  #worked this out on papre

# Limit below which we care about exposure for O2
#O2_limit = 7
#O2_limit = 2.2
O2_limit_list = [2.2,3.1,4.1,6]
pH_limit_list = [7.5,7.6,7.7,7.8,7.9,8,8.1,8.2,8.3]
#pH_limit_list = [7.6,7.7,7.8,8,8.5,9]
#pH_limit_list = [7.6,7.7,7.8,9]
#pH_limit_list = [7.6,7.7,7.8]
#---------------------------------------------------------------------
#---------------------------------------------------------------------

base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

lon_field = np.array(dset['lon_rho'])
lat_field = np.array(dset['lat_rho'])

dset.close

bounding_boxes_base = base_path + 'practice/bounding_boxes/create_boxes/'
bounding_boxes_continent_dir = bounding_boxes_base + 'continent/z_output/'
bounding_boxes_islands_dir = bounding_boxes_base + 'modify_islands/z_output/'
#bounding_boxes_islands_dir = bounding_boxes_base + 'aa_islands/z_output/'


tracking_output_dir = tracking_output_base + tracking_output_dir_pre
tracking_output_files = [f for f in listdir(tracking_output_dir) if isfile(join(tracking_output_dir,f))]
tracking_output_files.sort()


save_output_file_name = "pdf_data_output_seasonal_ranges_O2_pH___pld_{}_{}_".format(first_settlement_day,last_settlement_day) + tracking_output_dir_pre[0:-1]

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
#trajectory_status = status_all[0,:]
#trajectory_mask = trajectory_status == 0
#settlement_window_start = int(timesteps_per_day * first_settlement_day + 1)
#settlement_window_start = int(timesteps_per_day * (first_settlement_day+1))
#settlement_window_start = int(timesteps_per_day * first_settlement_day)

## Determine the total number of timesteps in the settlement window
#total_number_timesteps = int(np.sum(trajectory_mask))
#timesteps_settlement_window = total_number_timesteps - settlement_window_start

timesteps_settlement_window = pld_length_days * timesteps_per_day
#timesteps_full_run = (last_settlement_day - 1) * timesteps_per_day
timesteps_full_run = last_settlement_day * timesteps_per_day + 1
#timesteps_full_run = last_settlement_day * timesteps_per_day

#settlement_window_end = settlement_window_start + timesteps_settlement_window

first_settle_dex = first_settlement_day * timesteps_per_day 
#last_settle_dex = last_settlement_day * timesteps_per_day 
# Make adjustment for the fact that the 0th element in our tracking data is for time 0, ie initial condition
#first_settle_dex = first_settlement_day * timesteps_per_day + 1
last_settle_dex = last_settlement_day * timesteps_per_day + 1

## Add calculation of distribution of when bio windows open (to compare with when settlement actually happens; expecting "drift" in time due to physics, ie skew)
#bio_window_opening_distribution = np.zeros((timesteps_settlement_window))


#---------------------------------------------------------------------
#---------------------------------------------------------------------
# Prepare the data structure (2D array) for saving the pdf data

bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_psi_coastline_wc15n_continent.p'
#bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

n_boxes = 0
for box_lonlat in boxes_lonlat:
    n_boxes += 1

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

# number of pdfs per feild (4 seasonal and 1 overall = 5)
n_pdfs = 5

# Connectivity (release box number vs settlement box number)
pdf_arrays_connectivity = np.zeros((n_pdfs,n_boxes,n_boxes))

# Time after PLD until settlement (saving only release location) (release box number vs settlement time)
pdf_arrays_settleTime = np.zeros((n_pdfs,n_boxes,timesteps_settlement_window))

# Number of days eposed to DO levels below 2.2 (saving only settlement location) (release box number vs exposure time)
# note: Think the time dimension needs to be one bigger than the number of possible timesteps (ie need to include an option for "zero") 
pdf_arrays_O2 = np.zeros((len(O2_limit_list),n_pdfs,n_boxes,timesteps_full_run))

# Same idea for pH
pdf_arrays_pH = np.zeros((len(pH_limit_list),n_pdfs,n_boxes,timesteps_full_run))

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
pdf_arrays_T = np.zeros((n_pdfs,n_boxes,n_T_steps))

#---------------------------------------------------------------------
#---------------------------------------------------------------------
num_files = len(tracking_output_files)

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
# START THE MAIN LOOP!!!
#---------------------------------------------------------------------

file_number = 0

for tracking_output_file_pre in tracking_output_files:
    
    #file_number += 1
    
    ###TESTING
    #if file_number != 177:
#    if file_number not in [155,156,157]:
#    #if file_number != 156:
#        continue

    
    tracking_output_file = tracking_output_dir + tracking_output_file_pre

    dset = netCDF4.Dataset(tracking_output_file, 'r')

    particle_labels = dset.variables['trajectory'][:]
    lon_all = dset.variables['lon'][:]
    lat_all = dset.variables['lat'][:]
    #z_all = dset.variables['z'][:]
    status_all = dset.variables['status'][:]
    time = np.array(dset['time'])
    # Exposure variables 
    O2_all = dset.variables['oxygen'][:]
    pH_all = dset.variables['pH'][:]
    temp_all = dset.variables['sea_water_temperature'][:]

    dset.close()

    O2_all *= conversion_factor


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

    # Create array to store all trajectory locations of all particles during their settlement window
    drift_lons = np.zeros((num_particles,timesteps_settlement_window))
    drift_lats = np.zeros((num_particles,timesteps_settlement_window))

    drift_O2 = np.zeros((num_particles,timesteps_full_run))
    drift_pH = np.zeros((num_particles,timesteps_full_run))
    drift_T = np.zeros((num_particles,timesteps_full_run))
    #drift_O2 = np.zeros((num_particles,timesteps_settlement_window))
    #drift_pH = np.zeros((num_particles,timesteps_settlement_window))
    #drift_T = np.zeros((num_particles,timesteps_settlement_window))

    starting_lons = []
    starting_lats = []
    seed_months = []

    #for particle_label in particle_labels:
    for particle_id in range(len(particle_labels)):
        #---------------------------------------------------------------------
        # indent here
        
        trajectory_status = status_all[particle_id,:]

        # Store month of first timestep of trajectory (ie seeding/starting month)
        seed_months.append(run_seed_months_list[np.where(trajectory_status == 0)[0][0]])

        trajectory_mask = trajectory_status == 0

           
        # Trim the trajectories to prepare for processing!
        particle_lon = lon_all[particle_id,trajectory_mask]
        particle_lat = lat_all[particle_id,trajectory_mask]
        particle_O2 = O2_all[particle_id,trajectory_mask]
        particle_pH = pH_all[particle_id,trajectory_mask]
        particle_T = temp_all[particle_id,trajectory_mask]

        # Get the STARTING coordinates of each particle
        starting_lons.append(particle_lon[0]) 
        starting_lats.append(particle_lat[0]) 
        
        ## Now that initial positions are known, cut out the "drifting window" and add what remains as a row
        ## in the <drift_lons>, <drift_lats> arrays
        #drift_lons[particle_id,:] = particle_lon[settlement_window_start:]
        #drift_lats[particle_id,:] = particle_lat[settlement_window_start:]

        #drift_O2[particle_id,:] = particle_O2[settlement_window_start:]
        #drift_T[particle_id,:] = particle_T[settlement_window_start:]
        
        drift_lons[particle_id,:] = particle_lon[first_settle_dex:last_settle_dex]
        drift_lats[particle_id,:] = particle_lat[first_settle_dex:last_settle_dex]
        drift_O2[particle_id,:] = particle_O2[0:last_settle_dex]
        drift_pH[particle_id,:] = particle_pH[0:last_settle_dex]
        drift_T[particle_id,:] = particle_T[0:last_settle_dex]
        #drift_O2[particle_id,:] = particle_O2[1:last_settle_dex]
        #drift_pH[particle_id,:] = particle_pH[1:last_settle_dex]
        #drift_T[particle_id,:] = particle_T[1:last_settle_dex]
        
        #drift_O2[particle_id,:] = particle_O2[settlement_window_start:settlement_window_end]
        #drift_pH[particle_id,:] = particle_pH[settlement_window_start:settlement_window_end]
        #drift_T[particle_id,:] = particle_T[settlement_window_start:settlement_window_end]

    # prepare lists to hold the starting/ending box numbers for each particle
    initial_boxes = np.zeros(num_particles)
    settlement_boxes = np.zeros(num_particles)
    # add settlement time storage
    settlement_times = np.zeros(num_particles)

    # Exposure statistics
    particle_arrays_O2 = np.zeros((len(O2_limit_list),num_particles))
    particle_arrays_pH = np.zeros((len(pH_limit_list),num_particles))  
    particle_array_T = np.zeros(num_particles)
    particle_array_driftTime = np.zeros(num_particles)


    #---------------------------------------------------------------------
    # FIRST MUST DETERMINE STARTING LOCATIONS
    #---------------------------------------------------------------------

    # create empty list to store all of the (starting) lat/lon pairs as tuples
    #points_lon_lat = []
    #for ii in range(num_particles):
    #    points_lon_lat.append((starting_lons[ii],starting_lats[ii]))
    #points_lon_lat = np.array(points_lon_lat)

    points_lon_lat = np.zeros((num_particles,2))
    for ii in range(num_particles):
        points_lon_lat[ii,0] = starting_lons[ii]
        points_lon_lat[ii,1] = starting_lats[ii]


    # Need a running "box_dex" index to keep track of box numbers across the calculations
    # Maybe don't have a "zero" box, so that 0 can mean NULL....
    box_dex = 0
    #box_dex = 1

    # WAIT... ISLANDS FIST, SO THEY'RE AT THE BOTTOM CORNER OF THE PDF PLOT...?!
    num_islands = 8
    num_last_blob_island = 4

    for island_dex in range(num_islands,num_last_blob_island-1,-1):
    #for island_dex in range(num_last_blob_island,num_islands+1):

        bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}.p'.format(island_dex)

        # Load the boxes
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close        

        #for box_lonlat in boxes_lonlat:
        for box_lonlat in reversed(boxes_lonlat):
            box_dex += 1
            if box_lonlat is not None:
                path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                particles_inside_flags = path.contains_points(points_lon_lat)
                initial_boxes = initial_boxes + (box_dex * particles_inside_flags)
                #print(np.sum(particles_inside_flags))    


    # CONTINENT NEXT!!
    bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_psi_coastline_wc15n_continent.p'
    #bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
    file = open(bounding_boxes_file_in,'rb')
    boxes_lonlat = pickle.load(file)
    file.close

    for box_lonlat in boxes_lonlat:
        box_dex += 1
        if box_lonlat is not None:
            path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
            particles_inside_flags = path.contains_points(points_lon_lat)
            initial_boxes = initial_boxes + (box_dex * particles_inside_flags)
            #box_dex += 1
            #print(np.sum(particles_inside_flags))    





    # NOW DETERMINE SETTLEMENT LOCATIONS!

    # create the "safety mask" that I'll use to make sure I only store the first box entered during the settlement window
    settlement_safety_mask = np.ones(num_particles)

    ## Sample the settlement window distribution for random settlement window opening times!
    #bio_windows_pre1 = biological_window_truncNorm_distribution.rvs(num_particles)
    #bio_windows = np.round(bio_windows_pre1)
    ## I think this actually belongs out here - mask needs to become more open with time
    #timestep_bio_window_mask=np.full(np.shape(bio_windows)[0],False)

    
    for time_dex in range(timesteps_full_run):
    #for time_dex in range(timesteps_settlement_window):

        print("file {}/{}, timestep {}/{}".format(file_number+1, num_files, time_dex,timesteps_full_run-1))
        #print("file {}/{}, timestep {}/{}".format(file_number+1, num_files, time_dex+1,timesteps_full_run))
        #print("file {}/{}, timestep {}/{}".format(file_number+1, num_files, time_dex+1,timesteps_settlement_window))

        #------------------------------------------------------
        # INDENT HERE

        # JUST FOR TESTING
        #time_dex = 0  # TESTING
    
        current_O2 = drift_O2[:,time_dex]
        current_pH = drift_pH[:,time_dex]
        current_T = drift_T[:,time_dex]

        # Exposure 
        for ii in range(len(O2_limit_list)):
            particle_arrays_O2[ii,:] = particle_arrays_O2[ii,:] + ((current_O2 < O2_limit_list[ii]).astype(int) * settlement_safety_mask)
            #particle_arrays_O2[ii] = particle_arrays_O2[ii] + ((current_O2 < O2_limit_list[ii]).astype(int) * settlement_safety_mask)
        for ii in range(len(pH_limit_list)):
            particle_arrays_pH[ii,:] = particle_arrays_pH[ii,:] + ((current_pH < pH_limit_list[ii]).astype(int) * settlement_safety_mask)
            #particle_arrays_pH[ii] = particle_arrays_pH[ii] + ((current_pH < pH_limit_list[ii]).astype(int) * settlement_safety_mask)
        particle_array_T = particle_array_T + (current_T * settlement_safety_mask)
        particle_array_driftTime = particle_array_driftTime + settlement_safety_mask
        
        

        #------------------------------------------------------
        #------------------------------------------------------
        # New modification: we want to track exposure for ENTIRE lives of larvae.  Hence the time condition on settlement computation
        #------------------------------------------------------
        if time_dex >= first_settle_dex:
            print("settle time dex: {}".format(time_dex))
        #------------------------------------------------------
        #------------------------------------------------------
        #------------------------------------------------------
        

            settle_window_dex = time_dex - first_settle_dex

            current_lons = drift_lons[:,settle_window_dex] 
            current_lats = drift_lats[:,settle_window_dex] 
            
            #points_lon_lat = []
            #for ii in range(num_particles):
            #    points_lon_lat.append((current_lons[ii],current_lats[ii]))
            #points_lon_lat = np.array(points_lon_lat)

            points_lon_lat = np.zeros((num_particles,2))
            for ii in range(num_particles):
                points_lon_lat[ii,0] = starting_lons[ii]
                points_lon_lat[ii,1] = starting_lats[ii]

            # Need a running "box_dex" index to keep track of box numbers across the calculations
            # Maybe don't have a "zero" box, so that 0 can mean NULL....
            box_dex = 0
            #box_dex = 1

            # WAIT... ISLANDS FIST, SO THEY'RE AT THE BOTTOM CORNER OF THE PDF PLOT...?!
            num_islands = 8
            num_last_blob_island = 4

            for island_dex in range(num_islands,num_last_blob_island-1,-1):
            #for island_dex in range(num_last_blob_island,num_islands+1):

                bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}.p'.format(island_dex)

                # Load the boxes
                file = open(bounding_boxes_file_in,'rb')
                boxes_lonlat = pickle.load(file)
                file.close        

                #for box_lonlat in boxes_lonlat:
                for box_lonlat in reversed(boxes_lonlat):
                    box_dex += 1
                    if box_lonlat is not None:
                        path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                        particles_inside_flags = path.contains_points(points_lon_lat)

                        settlement_boxes = settlement_boxes + (box_dex * particles_inside_flags) * settlement_safety_mask
                        settlement_times = settlement_times + (settle_window_dex * particles_inside_flags) * settlement_safety_mask
                        #settlement_times = settlement_times + (time_dex * particles_inside_flags) * settlement_safety_mask
                        
                        ## record when settler bio windows opened (NOT settlement time)
                        #settlers_assigned_bio_windows[:,file_number] = settlers_assigned_bio_windows[:,file_number] + particles_inside_flags * settlement_safety_mask * timestep_bio_window_mask * (bio_windows+1)
                        ## record actual settle time of settlers
                        #settlers_timestep_settled[:,file_number] = settlers_timestep_settled[:,file_number] + particles_inside_flags * settlement_safety_mask * timestep_bio_window_mask * (time_dex+1)
        
        #------------------------------------------------------
        # TESTING
        #------------------------------------------------------
        #------------------------------------------------------
                        #settlement_boxes_test_array[:,time_dex] = (box_dex * particles_inside_flags) * settlement_safety_mask * timestep_bio_window_mask
                        #settlement_times_test_array[:,time_dex] = (time_dex * particles_inside_flags) * settlement_safety_mask * timestep_bio_window_mask
        #------------------------------------------------------
        #------------------------------------------------------
        #------------------------------------------------------

                        # Update the counter of settled particles.  For checking consistency
                        #settleCount += sum(settlement_safety_mask * particles_inside_flags)
                        counter_array[:,file_number] += particles_inside_flags * settlement_safety_mask
                        #counter_array[:,file_number] += particles_inside_flags * settlement_safety_mask * timestep_bio_window_mask
                        
                        
                        #print('\n')
                        #print(num_particles)
                        #print(np.sum(settlement_safety_mask))
                        #print(np.sum(timestep_bio_window_mask)) 
                        #print('hi')

                        # Update the safety mask, so that settlement prevents further modifications to the stored settlement location
                        safety_mask_modifyer = ~particles_inside_flags
                        #safety_mask_modifyer = ~particles_inside_flags + ~timestep_bio_window_mask
                        settlement_safety_mask = settlement_safety_mask * safety_mask_modifyer
                        #settlement_safety_mask = settlement_safety_mask * ~particles_inside_flags
                        


            # CONTINENT NEXT!!
            bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_psi_coastline_wc15n_continent.p'
            #bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
            file = open(bounding_boxes_file_in,'rb')
            boxes_lonlat = pickle.load(file)

            for box_lonlat in boxes_lonlat:
                box_dex += 1
                if box_lonlat is not None:
                    path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                    particles_inside_flags = path.contains_points(points_lon_lat)

                    settlement_boxes = settlement_boxes + (box_dex * particles_inside_flags) * settlement_safety_mask
                    settlement_times = settlement_times + (settle_window_dex * particles_inside_flags) * settlement_safety_mask
                    #settlement_times = settlement_times + (time_dex * particles_inside_flags) * settlement_safety_mask
            
                    ## record setter bio windows opened (NOT settlement time)
                    #settlers_assigned_bio_windows[:,file_number] = settlers_assigned_bio_windows[:,file_number] + particles_inside_flags * settlement_safety_mask * timestep_bio_window_mask * (bio_windows+1)
                        
                    ## record actual settle time of settlers
                    #settlers_timestep_settled[:,file_number] = settlers_timestep_settled[:,file_number] + particles_inside_flags * settlement_safety_mask * timestep_bio_window_mask * (time_dex+1)
                    

            #------------------------------------------------------
            # TESTING
            #------------------------------------------------------
            #------------------------------------------------------
                    #settlement_boxes_test_array[:,time_dex] = (box_dex * particles_inside_flags) * settlement_safety_mask * timestep_bio_window_mask
                    #settlement_times_test_array[:,time_dex] = (time_dex * particles_inside_flags) * settlement_safety_mask * timestep_bio_window_mask
            #------------------------------------------------------
            #------------------------------------------------------
            #------------------------------------------------------
                    
                    # Update the counter of settled particles.  For checking consistency
                    counter_array[:,file_number] += particles_inside_flags * settlement_safety_mask
                    #counter_array[:,file_number] += particles_inside_flags * settlement_safety_mask * timestep_bio_window_mask

                    # Update the safety mask, so that settlement prevents further modifications to the stored settlement location
                    safety_mask_modifyer = ~particles_inside_flags
                    #safety_mask_modifyer = ~particles_inside_flags + ~timestep_bio_window_mask
                    settlement_safety_mask = settlement_safety_mask * safety_mask_modifyer
                    #settlement_safety_mask = settlement_safety_mask * ~particles_inside_flags
                    
            #bio_window_opening_distribution[time_dex] = np.sum(settlers_assigned_bio_windows == ii)


    # Compute average temperature along trajectories
    average_T = [int(round(a/b, n_decimals_round) * T_scale_factor) for a,b in zip(particle_array_T, particle_array_driftTime)]

    # modify the pdf data structure
    for ii in range(num_particles):

        # wait we have 0's in here, so my logic requires we skip in this case
        if int(initial_boxes[ii]) == 0 or int(settlement_boxes[ii]) == 0:
            continue
        else:
       
            # Exposure 
            pdf_arrays_T[0,int(initial_boxes[ii])-1,average_T[ii]] += 1   
            for jj in range(len(O2_limit_list)):
                pdf_arrays_O2[jj,0,int(initial_boxes[ii])-1,int(particle_arrays_O2[jj,ii])] += 1   
                #pdf_arrays_O2[jj:0:int(initial_boxes[ii])-1,int(particle_arrays_O2[jj:ii])] += 1   
            for jj in range(len(pH_limit_list)):
                pdf_arrays_pH[jj,0,int(initial_boxes[ii])-1,int(particle_arrays_pH[jj,ii])] += 1   
                #pdf_arrays_pH[jj:0:int(initial_boxes[ii])-1,int(particle_arrays_pH[jj:ii])] += 1   
            pdf_arrays_connectivity[0,int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
            pdf_arrays_settleTime[0,int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
                
            #MAM
            if seed_months[ii] >=3 and seed_months[ii] <=5 : 
                pdf_arrays_T[2,int(initial_boxes[ii])-1,average_T[ii]] += 1   
                for jj in range(len(O2_limit_list)):
                    pdf_arrays_O2[jj,2,int(initial_boxes[ii])-1,int(particle_arrays_O2[jj,ii])] += 1   
                for jj in range(len(pH_limit_list)):
                    pdf_arrays_pH[jj,2,int(initial_boxes[ii])-1,int(particle_arrays_pH[jj,ii])] += 1   
                pdf_arrays_connectivity[2,int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
                pdf_arrays_settleTime[2,int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
            #JJA
            elif seed_months[ii] >=6 and seed_months[ii] <=8 : 
                pdf_arrays_T[3,int(initial_boxes[ii])-1,average_T[ii]] += 1   
                for jj in range(len(O2_limit_list)):
                    pdf_arrays_O2[jj,3,int(initial_boxes[ii])-1,int(particle_arrays_O2[jj,ii])] += 1   
                for jj in range(len(pH_limit_list)):
                    pdf_arrays_pH[jj,3,int(initial_boxes[ii])-1,int(particle_arrays_pH[jj,ii])] += 1   
                pdf_arrays_connectivity[3,int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
                pdf_arrays_settleTime[3,int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
            #SON
            elif seed_months[ii] >=9 and seed_months[ii] <=11 : 
                pdf_arrays_T[4,int(initial_boxes[ii])-1,average_T[ii]] += 1   
                for jj in range(len(O2_limit_list)):
                    pdf_arrays_O2[jj,4,int(initial_boxes[ii])-1,int(particle_arrays_O2[jj,ii])] += 1   
                for jj in range(len(pH_limit_list)):
                    pdf_arrays_pH[jj,4,int(initial_boxes[ii])-1,int(particle_arrays_pH[jj,ii])] += 1   
                pdf_arrays_connectivity[4,int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
                pdf_arrays_settleTime[4,int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
            #DJF
            else:
                pdf_arrays_T[1,int(initial_boxes[ii])-1,average_T[ii]] += 1   
                for jj in range(len(O2_limit_list)):
                    pdf_arrays_O2[jj,1,int(initial_boxes[ii])-1,int(particle_arrays_O2[jj,ii])] += 1   
                for jj in range(len(pH_limit_list)):
                    pdf_arrays_pH[jj,1,int(initial_boxes[ii])-1,int(particle_arrays_pH[jj,ii])] += 1   
                pdf_arrays_connectivity[1,int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
                pdf_arrays_settleTime[1,int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   



#            # Exposure 
#            pdf_arrays_T[0][int(initial_boxes[ii])-1,average_T[ii]] += 1   
#            for jj in range(len(O2_limit_list)):
#                pdf_arrays_O2[jj][0][int(initial_boxes[ii])-1,int(particle_arrays_O2[jj][ii])] += 1   
#            for jj in range(len(pH_limit_list)):
#                pdf_arrays_pH[jj][0][int(initial_boxes[ii])-1,int(particle_arrays_pH[jj][ii])] += 1   
#            pdf_arrays_connectivity[0][int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
#            pdf_arrays_settleTime[0][int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
#                
#            #MAM
#            if seed_months[ii] >=3 and seed_months[ii] <=5 : 
#                pdf_arrays_T[2][int(initial_boxes[ii])-1,average_T[ii]] += 1   
#                for jj in range(len(O2_limit_list)):
#                    pdf_arrays_O2[jj][2][int(initial_boxes[ii])-1,int(particle_arrays_O2[jj][ii])] += 1   
#                for jj in range(len(pH_limit_list)):
#                    pdf_arrays_pH[jj][2][int(initial_boxes[ii])-1,int(particle_arrays_pH[jj][ii])] += 1   
#                pdf_arrays_connectivity[2][int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
#                pdf_arrays_settleTime[2][int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
#            #JJA
#            elif seed_months[ii] >=6 and seed_months[ii] <=8 : 
#                pdf_arrays_T[3][int(initial_boxes[ii])-1,average_T[ii]] += 1   
#                for jj in range(len(O2_limit_list)):
#                    pdf_arrays_O2[jj][3][int(initial_boxes[ii])-1,int(particle_arrays_O2[jj][ii])] += 1   
#                for jj in range(len(pH_limit_list)):
#                    pdf_arrays_pH[jj][3][int(initial_boxes[ii])-1,int(particle_arrays_pH[jj][ii])] += 1   
#                pdf_arrays_connectivity[3][int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
#                pdf_arrays_settleTime[3][int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
#            #SON
#            elif seed_months[ii] >=9 and seed_months[ii] <=11 : 
#                pdf_arrays_T[4][int(initial_boxes[ii])-1,average_T[ii]] += 1   
#                for jj in range(len(O2_limit_list)):
#                    pdf_arrays_O2[jj][4][int(initial_boxes[ii])-1,int(particle_arrays_O2[jj][ii])] += 1   
#                for jj in range(len(pH_limit_list)):
#                    pdf_arrays_pH[jj][4][int(initial_boxes[ii])-1,int(particle_arrays_pH[jj][ii])] += 1   
#                pdf_arrays_connectivity[4][int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
#                pdf_arrays_settleTime[4][int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
#            #DJF
#            else:
#                pdf_arrays_T[1][int(initial_boxes[ii])-1,average_T[ii]] += 1   
#                for jj in range(len(O2_limit_list)):
#                    pdf_arrays_O2[jj][1][int(initial_boxes[ii])-1,int(particle_arrays_O2[jj][ii])] += 1   
#                for jj in range(len(pH_limit_list)):
#                    pdf_arrays_pH[jj][1][int(initial_boxes[ii])-1,int(particle_arrays_pH[jj][ii])] += 1   
#                pdf_arrays_connectivity[1][int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
#                pdf_arrays_settleTime[1][int(initial_boxes[ii])-1,int(settlement_times[ii])] += 1   
#



    #for ii in range(timesteps_settlement_window):
    #    bio_window_opening_distribution[ii] = bio_window_opening_distribution[ii] + np.sum(settlers_assigned_bio_windows[:,file_number] == ii+1)
        
    file_number += 1
       


d = {}
#d['settlers_timestep_settled'] = settlers_timestep_settled
#d['settlers_assigned_bio_windows'] = settlers_assigned_bio_windows
#d['bio_window_opening_distribution'] = bio_window_opening_distribution
d['pdf_arrays_T'] = pdf_arrays_T
#d['pdf_arrays_T'] = pdf_arrays_T
d['pdf_arrays_O2'] = pdf_arrays_O2
d['pdf_arrays_pH'] = pdf_arrays_pH
d['pdf_arrays_connectivity'] = pdf_arrays_connectivity
d['pdf_arrays_settleTime'] = pdf_arrays_settleTime
d['counter_array'] = counter_array
d['O2_limit_list'] = O2_limit_list
d['pH_limit_list'] = pH_limit_list

np.savez(save_output_file, **d)


