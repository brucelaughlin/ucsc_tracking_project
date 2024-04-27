# V2 - I'll try going box by box, running all particles... wait...

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
tracking_output_files = [f for f in listdir(output_dir) if isfile(join(output_dir,f))]
tracking_output_files.sort()


#---------------------------------------------------------------------
#---------------------------------------------------------------------


#for tracking_file in tracking_output_files:
#---------------------------------------------------------------------
# indent here

# just for testing
tracking_file = tracking_output_files[0] # JUST FOR TESTING

dset = netCDF4.Dataset(tracking_output_path, 'r')

#particle_labels = dset.variables['trajectory'][:]
lon_all = dset.variables['lon'][:]
lat_all = dset.variables['lat'][:]
#z_all = dset.variables['z'][:]
status_all = dset.variables['status'][:]

status_mask = status_all == 0




#---------------------------------------------------------------------
# Prepare the data structure (2D array) for saving the pdf data

n_boxes = 0

# Continent 
bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

# Weird operation needed here to check dimensions, since I used 2D lists for the boxes...
n_boxes = n_boxes + np.max([len(boxes_lonlat),len(boxes_lonlat[0])])

num_islands = 8
num_last_blob_island = 4
for island_dex in range(num_last_blob_island,num_islands+1):

    for inoffshore_switch in range(0,2):

        if inoffshore_switch == 0:
            bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)

        # Load the boxes
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close        

        n_boxes = n_boxes + np.max([len(boxes_lonlat),len(boxes_lonlat[0])])

# Store the raw binned data here
pdf_raw = np.zeros((n_boxes,n_boxes))

# NOW BEGIN THE BINNING!


# CONTINENT FIRST!!



# Continent 
bounding_boxes_file_in = bounding_boxes_continent_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close




#for particle_id in particle_labels:
#---------------------------------------------------------------------
# indent here

# just for testing
particle_id = 1 # JUST FOR TESTING

trajectory_status = status[particle_id,:]

trajectory_mask = trajectory_status == 0

# Determine the output frequency, n per day.
# Determine the timestep at which the settlement window opens
if particle_id == 1:
    timesteps_per_day = sum(trajectory_mask)/run_length_days
    if timesteps_per_day%1 != 0: sys.exit('(run timesteps)/(run_length_days) was not an integer!')
    settlement_window_start = int(timesteps_per_day * first_settlement_day)
   
# Trim the trajectories to prepare for processing!
particle_lon = lon_all[particle_id,trajectory_mask]
particle_lat = lat_all[particle_id,trajectory_mask]

particle_lon = particle_lon[settlement_window_start:]
particle_lat = particle_lat[settlement_window_start:]



# Continent


particles_initial_box_continent = []
particles_final_box_continent = []


# each "box" is a 2 by n array, with the first column being "i" coordinates, 2nd being "j"

box_dex = 0

for box_lonlat in boxes_lonlat:
#for ii in range(3,len(boxes_lonlat)-3):
    #box_lonlat = boxes_lonlat[ii]
    #box_dex += 1
    
    if box_lonlat is None:
        print('box {} has value "None" ..!?'.format(box_dex-1))
    if box_lonlat is not None:

        path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
        
        #points_inside_flags = path.contains_points(points_lon_lat) 
        particles_initial_inside_flags = path.contains_points(particles_initial_lon_lat) 
        particles_final_inside_flags = path.contains_points(particles_final_lon_lat) 
        
        #particles_initial_inside = particles_initial_lon_lat[particles_initial_inside_flags]
        #particles_final_inside = particles_final_lon_lat[particles_final_inside_flags]
        particles_initial_inside = particle_labels[particles_initial_inside_flags]
        particles_final_inside = particle_labels[particles_final_inside_flags]
        
        
        #particles_box_lon_lat = np.array([particles_box_lon,particles_box_lat])
        #particles_in_boxes_lonlat_continent.append(particles_box_lon_lat)

        #particles_initial_box_continent.append(particles_initial_inside)
        #particles_final_box_continent.append(particles_final_inside)
        if len(particles_initial_inside) > 0 :
            particles_initial_box_continent.append(particles_initial_inside)
        else:
            particles_initial_box_continent.append(None)
        if len(particles_final_inside) > 0 :
            particles_final_box_continent.append(particles_final_inside)
        else:
            particles_final_box_continent.append(None)

    box_dex += 1



# Islands

particles_initial_box_islands_inshore = []
particles_final_box_islands_inshore = []
particles_initial_box_islands_offshore = []
particles_final_box_islands_offshore = []

num_islands = 8
num_last_blob_island = 4

for island_dex in range(num_last_blob_island,num_islands+1):

    for inoffshore_switch in range(0,2):

        if inoffshore_switch == 0:
            bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = bounding_boxes_islands_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)


        # Load the boxes
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close        


        for box_lonlat in boxes_lonlat:
            if box_lonlat is not None:

                path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                
                particles_initial_inside_flags = path.contains_points(particles_initial_lon_lat) 
                particles_final_inside_flags = path.contains_points(particles_final_lon_lat) 
                
                particles_initial_inside = particle_labels[particles_initial_inside_flags]
                particles_final_inside = particle_labels[particles_final_inside_flags]
                
                
                if inoffshore_switch == 0:
                    #particles_initial_box_islands_inshore.append(particles_initial_inside)
                    #particles_final_box_islands_inshore.append(particles_final_inside)
                    if len(particles_initial_inside) > 0 :
                        particles_initial_box_islands_inshore.append(particles_initial_inside)
                    else:
                        particles_initial_box_islands_inshore.append(None)
                    if len(particles_final_inside) > 0 :
                        particles_final_box_islands_inshore.append(particles_final_inside)
                    else:
                        particles_final_box_islands_inshore.append(None)
                else:
                    #particles_initial_box_islands_offshore.append(particles_initial_inside)
                    #particles_final_box_islands_offshore.append(particles_final_inside)
                    if len(particles_initial_inside) > 0 :
                        particles_initial_box_islands_offshore.append(particles_initial_inside)
                    else:
                        particles_initial_box_islands_offshore.append(None)
                    if len(particles_final_inside) > 0 :
                        particles_final_box_islands_offshore.append(particles_final_inside)
                    else:
                        particles_final_box_islands_offshore.append(None)




# Combine all seed and settlement information... May want to have separate files for islands, but start here.

particles_initial_box_combined = particles_initial_box_islands_inshore + particles_initial_box_islands_offshore + particles_initial_box_continent
particles_final_box_combined = particles_final_box_islands_inshore + particles_final_box_islands_offshore + particles_final_box_continent



#file = open(particles_in_boxes_file_out_combined,'wb')
#pickle.dump(particles_in_boxes_lonlat_combined,file)
#file.close()

#file = open(particles_in_boxes_file_out_combined_ij,'wb')
#pickle.dump(particles_in_boxes_ij_combined,file)
#file.close()




