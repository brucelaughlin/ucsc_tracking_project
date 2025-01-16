# rememberAllReleases - A new normalization to match Patrick's papers - we calulate the fraction of all released from a location that settled at a given
# location, rather then dividing only by the number of total settled

# v2: holy hell, I've been doing this wrong from the beginning.  I create the "drift_lon/lat" arrays, but those only contain data from within the pld.  BUT,
# I was erroniously using the first element of those as the release location.  Terrible!

# v1: copied form the pdrake v1 script.  but, now not studying connectivity - just want to investigate local settlement.
# we have strong local (1-1) settlement at all plds, and that's not present in Patrick's plots - so see if any of
# the particles are stationary, stuck, etc... should filter those out before calculating connectivity.
# So, store indices of those particles, for plotting...



# create seasonal pdfs (djf, etc)

# Note that "status" is 0 when the particle is active, and a large magnitude negative
# number when not.  (strange!)


#---------------------------------------------------------------------
#---------------------------------------------------------------------
# I/O
#---------------------------------------------------------------------
#tracking_output_dir_pre = 'drift_150_physics_only_AKs_1en5_v1/'
#---------------------------------------------------------------------

# CHANGE THIS ONCE YOU'RE RE-ARRANGED THE OUTPUT DIRECTORY STRUCTURE
#tracking_output_base = "/home/blaughli/tracking_project/zz_output/tracking_project_output_projections/y_projections_1990_2020_KEEP/"
#tracking_output_base = "/data/blaughli/copiedFiles/y_projections_1990_2020_KEEP/"
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
import argparse
from pathlib import Path


#---------------------------------------------------------------------
#---------------------------------------------------------------------
# PARAMETERS and CONSTANTS

# fix the tracking data directory and base year, since we only have one set of files from patrick
tracking_output_dir = '/home/blaughli/tracking_project/y_pdrake_data/fwd_data/sub_set/one_file'
#tracking_output_dir = '/home/blaughli/tracking_project/y_pdrake_data/fwd_data/sub_set'
#tracking_output_dir = '/home/blaughli/tracking_project/y_pdrake_data/fwd_data'
base_year = 1999

#---------------------------------------------------------------------
# Need to know the number of DAYS of each particle's life (fixed unless I change the 
# the deactivation time in the model code)
# NOTE: I believe that the extra point in time in all files is due to there being data saved at "time 0" - so,
# a '90 day run' with daily output will have 91 timesteps because initial state is saved.
#---------------------------------------------------------------------



# Create truncated normal distribution to draw from for settlement window openings
# Data taken from the report provided by Will (page 33, assuming mean is in the middle of PLD ranges, assuming ranges represent 3 stardard deviations)
#mu, sigma, lower, upper  = 120, 10, 90, 150



# WTF IS GOING ON HERE WITH THE TIMES???????

# Opendrift output times are seconds since Jan 1, 1979   (what??)
base_datetime = datetime.datetime(base_year,1,1,0,0,0)
#base_datetime = datetime.datetime(1988,1,1,0,0,0)


#---------------------------------------------------------------------
# define plds

pld_array = np.array([[5,6],[10,11],[15,17],[20,22],[30,33],[45,49],[60,65],[90,98],[120,131],[150,164],[180,197]])

# choose one pld to compare, for now
pld_chosen_dex = 5

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


tracking_output_files = [f for f in listdir(tracking_output_dir) if isfile(join(tracking_output_dir,f))]
tracking_output_files.sort()

# I always do this - is it bad practice?
tracking_output_dir = tracking_output_dir + "/"

save_output_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

#---------------------------------------------------------------------
#---------------------------------------------------------------------


extrema_lon = [np.min(lon_field),np.max(lon_field)]
extrema_lat = [np.min(lat_field),np.max(lat_field)]





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
# This step is for setting up the pdf data structure which will be modified with each Opendrift output file.
# Also set up constants used throughout the runtime.

# number of pdfs per feild (4 seasonal and 1 overall = 5)
# JUST MAKE THE ANNUAL FILE
n_pdfs = 1
#n_pdfs = 5


# Need to have a way to see if I'm doing this right... without double counting errors, etc
tracking_output_file = tracking_output_dir + tracking_output_files[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')
ocean_time = dset.variables['ocean_time'][:]
lon = dset.variables['lon'][:]
dset.close()
num_particles = np.shape(lon)[1]
num_files = len(tracking_output_files)
counter_array=np.zeros((num_particles,num_files))


print('NUMBER OF PARTICLES: {}'.format(num_particles))


timesteps_per_day = int(1/((ocean_time[1]-ocean_time[0])/86400))

# For now, exit if output is less than daily...
if timesteps_per_day < 1:
    sys.exit('This code is dumb and currently wants a save timestep of <= 1 day.  Should be an easy fix')




# For the histogram of average temperature experienced - just estimating range, since I don't know it without processing
#---------------------
# Make sure these match (0.1 = 1, 0.01 = 2, etc)
T_step = 0.1
n_decimals_round = 1
T_scale_factor = int(1/T_step)
#---------------------
T_min = 0
T_max = 30
n_T_steps = len(np.arange(T_min,T_max+1,T_step))



#---------------------------------------------------------------------
# START THE MAIN LOOP!!!
#---------------------------------------------------------------------

# This is hacked, assumes only one file

# store all local trajectories in a list... or dict
#local_trajectory_list = []
#local_trajectory_dict = {}
#local_trajectory_dict_lon = {}
#local_trajectory_dict_lat = {}
local_trajectory_lons = []
local_trajectory_lats = []
local_trajectory_indices = []

settle_time_indices = []



dummy_value = 9999

for pld_dex in range(len(pld_array)):
        
    ###TESTING
    # test the 45-49 day pld
    if pld_dex != pld_chosen_dex:
        continue
        #break

    first_settlement_day = pld_array[pld_dex,0]
    last_settlement_day = pld_array[pld_dex,1]

    print('pld: {}-{}'.format(first_settlement_day,last_settlement_day))

    # THIS is the v5 adjustment: need to only use data from the pld, which begins after "first_settlement_day" and ends after "last_settlement_day"
    pld_length_days = last_settlement_day - first_settlement_day + 1


    timesteps_settlement_window = pld_length_days * timesteps_per_day
#    timesteps_full_run = (last_settlement_day+1) * timesteps_per_day + 1 # why isn't this just taken from the dimensions of the files?


    #first_settle_dex = first_settlement_day * timesteps_per_day + 1
    first_settle_dex = first_settlement_day * timesteps_per_day  # Why was I adding 1 here????
    last_settle_dex = (last_settlement_day+1) * timesteps_per_day # And here????
    #last_settle_dex = (last_settlement_day+1) * timesteps_per_day + 1


    #---------------------------------------------------------------------
    # Create lists to store statistics for full run and seasonal subsets
    #---------------------------------------------------------------------

    # store the number of particles released from each box
    release_counts_per_cell = np.zeros((n_pdfs,n_boxes))


    # Connectivity (release box number vs settlement box number)
    pdf_arrays_connectivity = np.zeros((n_pdfs,n_boxes,n_boxes))

    # Time after PLD until settlement (saving only release location) (release box number vs settlement time)
    pdf_arrays_settleTime = np.zeros((n_pdfs,n_boxes,timesteps_settlement_window))

    # Number of days eposed to DO levels below 2.2 (saving only settlement location) (release box number vs exposure time)
    # note: Think the time dimension needs to be one bigger than the number of possible timesteps (ie need to include an option for "zero") 
    #pdf_arrays_O2 = np.zeros((len(O2_limit_list),n_pdfs,n_boxes,timesteps_full_run))

    # Same idea for pH
    #pdf_arrays_pH = np.zeros((len(pH_limit_list),n_pdfs,n_boxes,timesteps_full_run))

    # Histogram of average temperature experienced - just estimating range, since I don't know it without processing
    #pdf_arrays_T = np.zeros((n_pdfs,n_boxes,n_T_steps))

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------

    file_number = 0

    for tracking_output_file_pre in tracking_output_files:
       
        ###TESTING
        if file_number > 0:
            break
        

        print(tracking_output_file_pre)

            
        tracking_output_file = tracking_output_dir + tracking_output_file_pre

        dset = netCDF4.Dataset(tracking_output_file, 'r')

        #particle_labels = dset.variables['trajectory'][:]
        lon_all = dset.variables['lon'][:]
        lat_all = dset.variables['lat'][:]
        #z_all = dset.variables['z'][:]
        #status_all = dset.variables['status'][:]
        time = np.array(dset['ocean_time'])
        #time = np.array(dset['time'])
        # Exposure variables 
        #O2_all = dset.variables['oxygen'][:]
        #pH_all = dset.variables['pH'][:]
        #temp_all = dset.variables['sea_water_temperature'][:]

        dset.close()

        #O2_all *= conversion_factor


        # Store the total number of particles
        num_particles = np.shape(lon)[1]
        num_timesteps = np.shape(lon)[0]
        #num_particles = len(particle_labels)
         
        # Why not just make one array of all of the data, and then reference it by time index???
        particles_lon_all=np.zeros([num_particles,num_timesteps])
        particles_lat_all=np.zeros([num_particles,num_timesteps])
        for ii in range(num_particles):
            particle_lon = lon_all[:,ii]
            particle_lat = lat_all[:,ii]
            particle_lon = particle_lon[~particle_lon.mask].data
            particle_lat = particle_lat[~particle_lat.mask].data
            # should I just use vstack? Well,  would have the same issue that I address here!
            particles_lon_all[ii] = np.pad(particle_lon,(0,np.shape(particles_lon_all)[1]-len(particle_lon)), 'constant',constant_values=(dummy_value))
            particles_lat_all[ii] = np.pad(particle_lat,(0,np.shape(particles_lon_all)[1]-len(particle_lat)), 'constant',constant_values=(dummy_value))


        # prepare lists to hold the starting/ending box numbers for each particle
        release_boxes = np.zeros(num_particles).astype(int)
        settlement_boxes = np.zeros(num_particles).astype(int)
        # add settlement time storage
        settlement_times = np.zeros(num_particles).astype(int)


        #---------------------------------------------------------------------
        # FIRST MUST DETERMINE STARTING LOCATIONS
        #---------------------------------------------------------------------
            
        points_lon_lat = np.zeros((num_particles,2))
        points_lon_lat[:,0] = particles_lon_all[:,0]
        points_lon_lat[:,1] = particles_lat_all[:,0]

        #points_lon_lat = np.zeros((num_particles,2))
        #for particle_id in range(num_particles):
        #    particle_lon = lon_all[:,particle_id]
        #    particle_lat = lat_all[:,particle_id]
        #    particle_lon = particle_lon[~particle_lon.mask].data
        #    particle_lat = particle_lat[~particle_lat.mask].data
        #    points_lon_lat[particle_id,0] = particle_lon[0]
        #    points_lon_lat[particle_id,1] = particle_lat[0]


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
                    particles_inside_flags = path.contains_points(points_lon_lat).astype(int)
                    release_boxes = release_boxes + (box_dex * particles_inside_flags)
                    #print(np.sum(particles_inside_flags))    


        # CONTINENT NEXT!!
        bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_psi_coastline_wc15n_continent.p'
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close

        for box_lonlat in boxes_lonlat:
            box_dex += 1
            if box_lonlat is not None:
                path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                particles_inside_flags = path.contains_points(points_lon_lat).astype(int)
                release_boxes = release_boxes + (box_dex * particles_inside_flags)
                #print(np.sum(particles_inside_flags))    





        # NOW DETERMINE SETTLEMENT LOCATIONS!

        # create the "safety mask" that I'll use to make sure I only store the first box entered during the settlement window
        settlement_safety_mask = np.ones(num_particles).astype(int)





        # Wait, have I been ignoring the PLD's this whole time???
        # Oh no, my friend - it's worse than that...
        
        for time_dex in range(first_settle_dex,last_settle_dex):
        
        #for time_dex in range(timesteps_settlement_window):

            print("file {}/{}, timestep {}/{}".format(file_number+1, num_files, time_dex,last_settle_dex-1))
            #print("file {}/{}, timestep {}/{}".format(file_number+1, num_files, time_dex,timesteps_settlement_window-1))

            # BIG MISTAKE
            #current_lons = drift_lons[:,time_dex] 
            #current_lats = drift_lats[:,time_dex] 
            
            #points_lon_lat = np.zeros((num_particles,2))
            #for particle_id in range(num_particles):
            #    #points_lon_lat[ii,0] = current_lons[ii]
            #    #points_lon_lat[ii,1] = current_lats[ii]
            #    particle_lon = lon_all[:,particle_id]
            #    particle_lat = lat_all[:,particle_id]
            #    particle_lon = particle_lon[~particle_lon.mask].data
            #    particle_lat = particle_lat[~particle_lat.mask].data
   
  
            points_lon_lat = np.zeros((num_particles,2))
            points_lon_lat[:,0] = particles_lon_all[:,time_dex]
            points_lon_lat[:,1] = particles_lat_all[:,time_dex]

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
                        particles_inside_flags_int = particles_inside_flags.astype(int)

                        settlement_boxes = settlement_boxes + (box_dex * particles_inside_flags_int) * settlement_safety_mask
                        settlement_times = settlement_times + ((time_dex+1) * particles_inside_flags_int) * settlement_safety_mask
                        
                        # Update the counter of settled particles.  For checking consistency
                        counter_array[:,file_number] += particles_inside_flags_int * settlement_safety_mask
                        
       
                        # Store the local settlers!
                        settler_box_numbers = (box_dex * particles_inside_flags_int) * settlement_safety_mask
                        for ii in range(len(settler_box_numbers)):
                            if settler_box_numbers[ii] != 0:
                                if settler_box_numbers[ii] == release_boxes[ii]:
                                    #local_trajectory_lons.append(particles_lon_all[ii,time_dex])
                                    #local_trajectory_lats.append(particles_lat_all[ii,time_dex]) 
                                    local_trajectory_lons.append(particles_lon_all[ii,0:])
                                    local_trajectory_lats.append(particles_lat_all[ii,0:]) 
                                    local_trajectory_indices.append(ii)
                                    settle_time_indices.append(time_dex)

                        # Update the safety mask, so that settlement prevents further modifications to the stored settlement location
                        safety_mask_modifyer = ~particles_inside_flags
                        settlement_safety_mask = settlement_safety_mask * safety_mask_modifyer.astype(int)
                        


            # CONTINENT NEXT!!
            bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_psi_coastline_wc15n_continent.p'
            file = open(bounding_boxes_file_in,'rb')
            boxes_lonlat = pickle.load(file)

            for box_lonlat in boxes_lonlat:
                box_dex += 1
                if box_lonlat is not None:
                    path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                    particles_inside_flags = path.contains_points(points_lon_lat)
                    particles_inside_flags_int = particles_inside_flags.astype(int)

                    settlement_boxes = settlement_boxes + (box_dex * particles_inside_flags_int) * settlement_safety_mask
                    settlement_times = settlement_times + ((time_dex+1) * particles_inside_flags_int) * settlement_safety_mask
            
                    # Update the counter of settled particles.  For checking consistency
                    counter_array[:,file_number] += particles_inside_flags_int * settlement_safety_mask
                        
                    # Store the local settlers!
                    settler_box_numbers = (box_dex * particles_inside_flags_int) * settlement_safety_mask
                    for ii in range(len(settler_box_numbers)):
                        if settler_box_numbers[ii] != 0:
                            if settler_box_numbers[ii] == release_boxes[ii]:
                                #local_trajectory_lons.append(particles_lon_all[ii,time_dex])
                                #local_trajectory_lats.append(particles_lat_all[ii,time_dex]) 
                                local_trajectory_lons.append(particles_lon_all[ii,0:])
                                local_trajectory_lats.append(particles_lat_all[ii,0:])
                                local_trajectory_indices.append(ii)
                                settle_time_indices.append(time_dex)

                        
                    # Update the safety mask, so that settlement prevents further modifications to the stored settlement location
                    safety_mask_modifyer = ~particles_inside_flags
                    settlement_safety_mask = settlement_safety_mask * safety_mask_modifyer.astype(int)
                        


        # Compute average temperature along trajectories
        #average_T = [int(round(a/b, n_decimals_round) * T_scale_factor) for a,b in zip(particle_array_T, particle_array_driftTime)]

        num_good = 0
        num_bad = 0
        num_empty = 0
        num_outofbounds = 0

        # modify the pdf data structure
        for ii in range(num_particles):

                
            # Patrick only has the annual array
            array_dex_list = [0]
           
            
            # wait we have 0's in here, so my logic requires we skip in this case
            if release_boxes[ii] == 0 or settlement_boxes[ii] == 0:
                if release_boxes[ii] == 0:
                    if particles_lon_all[ii,0] == dummy_value:
                    #if particles_lon_all[ii,0] == 0:
                        num_empty += 1
                    elif particles_lon_all[ii,0] < extrema_lon[0] or particles_lon_all[ii,0] > extrema_lon[1] or particles_lat_all[ii,0] < extrema_lat[0] or  particles_lat_all[ii,0] > extrema_lat[1]:
                        num_outofbounds += 1
                    #elif particles_lon_all[ii,-1] == 0:
                    #    num_empty += 1
                num_bad += 1
                continue
            else:
                
                num_good += 1
                
                release_counts_per_cell[0,int(release_boxes[ii])-1] += 1
                   
                for array_dex in array_dex_list:
                    
                    
                    #if settlement_times[ii] > 0:  # I actually think this check is redundant, since we already filtered out particles that didn't settle
                    pdf_arrays_settleTime[array_dex,int(release_boxes[ii])-1,int(settlement_times[ii])-first_settle_dex-1] += 1   
                    #pdf_arrays_settleTime[array_dex,int(release_boxes[ii])-1,int(settlement_times[ii])-1] += 1   
                    
                    pdf_arrays_connectivity[array_dex,int(release_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   
            

        print('num_good: {}'.format(num_good))
        print('num_empty: {}'.format(num_empty))
        print('num_outofbounds: {}'.format(num_outofbounds))
        print('num_bad: {}'.format(num_bad))

        file_number += 1



    d = {}
    d['release_counts_per_cell'] = release_counts_per_cell
    d['pdf_arrays_connectivity'] = pdf_arrays_connectivity
    d['pdf_arrays_settleTime'] = pdf_arrays_settleTime
    d['counter_array'] = counter_array
    
    d['local_trajectory_lons'] = local_trajectory_lons
    d['local_trajectory_lats'] = local_trajectory_lats
    d['local_trajectory_indices'] = local_trajectory_indices

    d['pld_days'] = pld_array[pld_dex]
    d['settle_time_indices'] = settle_time_indices

    save_output_file_name_pre = "binned_data_seasonal_allReleases_baseYear_{}_".format(base_year)
    save_output_file_name = save_output_file_name_pre + tracking_output_dir.split('/')[-2]
    save_output_full_path = save_output_directory + save_output_file_name + "_pld_{}_{}_pdrake".format(pld_array[pld_dex,0],pld_array[pld_dex,1])
    
    np.savez(save_output_full_path, **d)







