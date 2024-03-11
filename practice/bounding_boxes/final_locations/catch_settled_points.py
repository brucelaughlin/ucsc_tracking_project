# Error - think I need to use lat/lon, as in version 1 I just used i/j which
# depends on the grid type... ie it's wrong to use i/j from a polygon in psi
# to bound rho points... 

import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as plt_path
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint

#-------------------- EDIT THESE -------------------------------------
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

bounding_boxes_dir = 'practice/bounding_boxes/create_boxes/'
bounding_boxes_file_in = 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
bounding_boxes_path = base_path + bounding_boxes_dir + bounding_boxes_file_in

tracking_output_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/v_test_output/x_results_1/vv_10_factor_correct_15dt_20day/'
tracking_output_file = 'test_output_floats_10000_saveDT_60_calcDT_015.nc'
tracking_output_path = tracking_output_dir + tracking_output_file
#---------------------------------------------------------------------
#---------------------------------------------------------------------

dset = netCDF4.Dataset(tracking_output_path, 'r')

particle_labels = dset.variables['trajectory'][:]
lon_all = dset.variables['lon'][:]
lat_all = dset.variables['lat'][:]
z_all = dset.variables['z'][:]

num_floats = np.shape(lon_all)[0]
lon_if = np.zeros((num_floats,2))
lat_if = np.zeros((num_floats,2))
z_if = np.zeros((num_floats,2))

lon_if[:,0] = lon_all[:,0]
lon_if[:,1] = lon_all[:,-1]
lat_if[:,0] = lat_all[:,0]
lat_if[:,1] = lat_all[:,-1]
z_if[:,0] = z_all[:,0]
z_if[:,1] = z_all[:,-1]



particles_initial_lonlat = []
particles_final_lonlat = []

for ii in range(num_floats):
    particles_initial_lon_lat.append((lon_if[ii,0],lat_if[ii,0]))
    particles_final_lon_lat.append((lon_if[ii,1],lat_if[ii,1]))


# Continent


bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

particles_initial_box_continent = []
particles_final_box_continent = []


# each "box" is a 2 by n array, with the first column being "i" coordinates, 2nd being "j"

box_dex = 0

for box_lonlat in boxes_lonlat:
#for ii in range(3,len(boxes_lonlat)-3):
    #box_lonlat = boxes_lonlat[ii]
    box_dex += 1
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
        particles_initial_box_continent.append(particles_initial_inside)
        particles_final_box_continent.append(particles_final_inside)
        




# Islands

particles_initial_box_islands_inshore = []
particles_final_box_islands_inshore = []
particles_initial_box_islands_offshore = []
particles_final_box_islands_offshore = []

num_islands = 8
num_last_blob_island = 4


for island_dex in range(num_last_blob_island,num_islands+1):

    # Set an index for the bounding point lists (the lists of particles used to split the coastlines and isolines)
    bp_dex = island_dex-num_last_blob_island

    for inoffshore_switch in range(0,2):

        if inoffshore_switch == 0:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)


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
                    particles_initial_box_islands_inshore.append(particles_initial_inside)
                    particles_final_box_islands_inshore.append(particles_final_inside)
                else:
                    particles_initial_box_islands_offshore.append(particles_initial_inside)
                    particles_final_box_islands_offshore.append(particles_final_inside)




# Combine all seed and settlement information... May want to have separate files for islands, but start here.

particles_initial_box_combined = particles_initial_box_islands_inshore + particles_initial_box_islands_offshore + particles_initial_box_continent
particles_initial_box_combined = particles_initial_box_islands_inshore + particles_initial_box_islands_offshore + particles_initial_box_continent

file = open(particles_in_boxes_file_out_combined,'wb')
pickle.dump(particles_in_boxes_lonlat_combined,file)
file.close()

file = open(particles_in_boxes_file_out_combined_ij,'wb')
pickle.dump(particles_in_boxes_ij_combined,file)
file.close()




