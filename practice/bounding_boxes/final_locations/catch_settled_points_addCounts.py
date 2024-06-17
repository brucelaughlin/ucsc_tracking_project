# Error - think I need to use lat/lon, as in version 1 I just used i/j which
# depends on the grid type... ie it's wrong to use i/j from a polygon in psi
# to bound rho points... 

# Note that "status" is 0 when the particle and active, and a large magnitude negative
# number when not.  (strange!)

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
# Need to know the number of DAYS of each particle's life (fixed unless I change the 
# the deactivation time in the model code)

run_length_days = 91


# Save the number of days in the drifting window before the settlement window opens
first_settlement_day = 30
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
bounding_boxes_islands_dir = bounding_boxes_base + 'aa_islands/z_output/'


tracking_output_dir = '/data03/blaughli/tracking_project_output/test2_physics_only/'
tracking_output_files = [f for f in listdir(tracking_output_dir) if isfile(join(tracking_output_dir,f))]
tracking_output_files.sort()

save_output_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'
save_output_file = save_output_directory + 'pdf_data_output.p'


#---------------------------------------------------------------------
# This step is for setting up the pdf data structure which will be modified with each Opendrift output file.
# Also set up constants used throughout the runtime.

tracking_output_file = tracking_output_dir + tracking_output_files[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')
status_all = dset.variables['status'][:]

# Determine the output frequency, n per day.
# Determine the timestep at which the settlement window opens
trajectory_status = status_all[0,:]
trajectory_mask = trajectory_status == 0
timesteps_per_day = trajectory_mask.sum()/run_length_days
if timesteps_per_day%1 != 0: sys.exit('(run timesteps)/(run_length_days) was not an integer!')
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

    for inoffshore_switch in range(0,2):

        if inoffshore_switch == 0:
            bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)

        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close        

        for box_lonlat in boxes_lonlat:
            n_boxes += 1
        #n_boxes += np.max([len(boxes_lonlat),len(boxes_lonlat[0])])

#---------------------------------------------------------------------
#---------------------------------------------------------------------
# Create the 2D array that will store the pdf data for the whole experiment
pdf_raw = np.zeros((n_boxes,n_boxes))
#---------------------------------------------------------------------
#---------------------------------------------------------------------


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
# START THE MAIN LOOP!!!
#---------------------------------------------------------------------

for tracking_output_file_pre in tracking_output_files:
    
    file_number += 1
    
    # TESTING
    #if file_number != 177:
    #    continue

    
    tracking_output_file = tracking_output_dir + tracking_output_file_pre

    dset = netCDF4.Dataset(tracking_output_file, 'r')

    particle_labels = dset.variables['trajectory'][:]
    lon_all = dset.variables['lon'][:]
    lat_all = dset.variables['lat'][:]
    #z_all = dset.variables['z'][:]
    status_all = dset.variables['status'][:]
    dset.close()

    # Store the total number of particles
    num_particles = len(particle_labels)
      
    # Determine the output frequency, n per day.
    # Determine the timestep at which the settlement window opens
    trajectory_status = status_all[0,:]
    trajectory_mask = trajectory_status == 0
    timesteps_per_day = trajectory_mask.sum()/run_length_days
    if timesteps_per_day%1 != 0: sys.exit('(run timesteps)/(run_length_days) was not an integer!')
    settlement_window_start = int(timesteps_per_day * first_settlement_day)

    # Determine the total number of timesteps in the settlement window
    total_number_timesteps = int(np.sum(trajectory_mask))
    timesteps_settlement_window = total_number_timesteps - settlement_window_start

    # Create array to store all trajectory locations of all particles during their settlement window
    drift_lons = np.zeros((num_particles,timesteps_settlement_window))
    drift_lats = np.zeros((num_particles,timesteps_settlement_window))


    starting_lons = []
    starting_lats = []

    #for particle_label in particle_labels:
    for particle_id in range(len(particle_labels)):
        #---------------------------------------------------------------------
        # indent here
        
        trajectory_status = status_all[particle_id,:]

        trajectory_mask = trajectory_status == 0

           
        # Trim the trajectories to prepare for processing!
        particle_lon = lon_all[particle_id,trajectory_mask]
        particle_lat = lat_all[particle_id,trajectory_mask]

        # Get the STARTING coordinates of each particle
        starting_lons.append(particle_lon[0]) 
        starting_lats.append(particle_lat[0]) 
        
        # Now that initial positions are known, cut out the "drifting window" and add what remains as a row
        # in the <drift_lons>, <drift_lats> arrays
        drift_lons[particle_id,:] = particle_lon[settlement_window_start:]
        drift_lats[particle_id,:] = particle_lat[settlement_window_start:]
        #particle_lon = particle_lon[settlement_window_start:]
        #particle_lat = particle_lat[settlement_window_start:]


    # prepare lists to hold the starting/ending box numbers for each particle
    initial_boxes = np.zeros(num_particles)
    settlement_boxes = np.zeros(num_particles)




    #---------------------------------------------------------------------
    # FIRST MUST DETERMINE STARTING LOCATIONS
    #---------------------------------------------------------------------

    # create empty list to store all of the (starting) lat/lon pairs as tuples
    points_lon_lat = []
    for ii in range(num_particles):
        points_lon_lat.append((starting_lons[ii],starting_lats[ii]))
    points_lon_lat = np.array(points_lon_lat)

    # Need a running "box_dex" index to keep track of box numbers across the calculations
    # Maybe don't have a "zero" box, so that 0 can mean NULL....
    box_dex = 0
    #box_dex = 1

    # WAIT... ISLANDS FIST, SO THEY'RE AT THE BOTTOM CORNER OF THE PDF PLOT...?!
    num_islands = 8
    num_last_blob_island = 4

    for island_dex in range(num_islands,num_last_blob_island-1,-1):
    #for island_dex in range(num_last_blob_island,num_islands+1):

        for inoffshore_switch in range(0,2):

            #if inoffshore_switch == 0:
            if inoffshore_switch == 1:
                bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
            else:
                bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)

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
    bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
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


    for time_dex in range(timesteps_settlement_window):

        #print("{}/{}".format(time_dex,timesteps_settlement_window))
        #print("{}/{}".format(time_dex+1,timesteps_settlement_window))
        print("file {}/{}, timestep {}/{}".format(file_number, num_files, time_dex+1,timesteps_settlement_window))

        #------------------------------------------------------
        # INDENT HERE

        # JUST FOR TESTING
        #time_dex = 0  # TESTING

        current_lons = drift_lons[:,time_dex] 
        current_lats = drift_lats[:,time_dex] 

        # create empty list to store all of the (current) lat/lon pairs as tuples
        points_lon_lat = []
        for ii in range(num_particles):
            points_lon_lat.append((current_lons[ii],current_lats[ii]))

        points_lon_lat = np.array(points_lon_lat)

        # Need a running "box_dex" index to keep track of box numbers across the calculations
        # Maybe don't have a "zero" box, so that 0 can mean NULL....
        box_dex = 0
        #box_dex = 1

        # WAIT... ISLANDS FIST, SO THEY'RE AT THE BOTTOM CORNER OF THE PDF PLOT...?!
        num_islands = 8
        num_last_blob_island = 4

        for island_dex in range(num_islands,num_last_blob_island-1,-1):
        #for island_dex in range(num_last_blob_island,num_islands+1):

            for inoffshore_switch in range(0,2):

                #if inoffshore_switch == 0:
                if inoffshore_switch == 1:
                    bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
                else:
                    bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)

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
                        
                        # Update the counter of settled particles.  For checking consistency
                        #settleCount += sum(settlement_safety_mask * particles_inside_flags)
                        counter_array[:,file_number-1] += particles_inside_flags * settlement_safety_mask

                        # Update the safety mask, so that settlement prevents further modifications to the stored settlement location
                        settlement_safety_mask = settlement_safety_mask * ~particles_inside_flags
                        
                        #print(np.sum(particles_inside_flags))
                        #print(num_particles- np.sum(settlement_safety_mask))
                        #print('\n')

                        #box_dex += 1


        # CONTINENT NEXT!!
        bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)

        for box_lonlat in boxes_lonlat:
            box_dex += 1
            if box_lonlat is not None:
                path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                particles_inside_flags = path.contains_points(points_lon_lat)

                settlement_boxes = settlement_boxes + (box_dex * particles_inside_flags) * settlement_safety_mask
                
                # Update the counter of settled particles.  For checking consistency
                #settleCount += sum(settlement_safety_mask * particles_inside_flags)
                counter_array[:,file_number-1] += particles_inside_flags * settlement_safety_mask

                # Update the safety mask, so that settlement prevents further modifications to the stored settlement location
                settlement_safety_mask = settlement_safety_mask * ~particles_inside_flags
                
                #print(np.sum(particles_inside_flags))
                #print(num_particles- np.sum(settlement_safety_mask))
                #print('\n')

                #box_dex += 1



    # modify the pdf data structure
    for ii in range(num_particles):

        # wait we have 0's in here, so my logic requires we skip in this case
        if int(initial_boxes[ii]) == 0 or int(settlement_boxes[ii]) == 0:
            continue
        else:
            pdf_raw[int(initial_boxes[ii])-1,int(settlement_boxes[ii])-1] += 1   





file = open(save_output_file,'wb')
#pickle.dump(pdf_raw,file)
pickle.dump([pdf_raw,counter_array],file)
file.close()



    #n_boxes_seeded = int(np.max(initial_boxes))
    #n_boxes_settled = int(np.max(settlement_boxes))
    #X = np.arange(-0.5, n_boxes_settled, 1)
    #Y = np.arange(-0.5, n_boxes_seeded, 1)
    #fig,ax = plt.subplots()
    ###ax.pcolormesh(pdf_raw)
    #ax.pcolormesh(X,Y,pdf_raw)
    #ax.set_xlabel("seeding box number")
    #ax.set_ylabel("settlement box number")
    #plt.title("PDF of settlement vs seed location")
    #plt.show()


