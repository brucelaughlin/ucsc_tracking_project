# Load the coastlines for the "blob" islands and insert artifical 1-D "bridges" between them,
# to be used for defining boxes

# Wait.... since we want an "inshore" and "offshore" side of each island, perhaps, for the blobs,
# I should just treat the upper coastline as its own coastline, and the same for the lower.

import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import ast

#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

base_path = '/home/blaughli/tracking_project/'
psi_bl_directory = 'practice/bounding_boxes/create_boxes/z_modify_psi/'
output_dir = 'z_output/'

grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_only_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in

psi_bl_file_in = 'mask_psi_bl_islands.p'
psi_bl_path_in = base_path + psi_bl_directory + psi_bl_file_in

dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_psi = 'psi'
lon_psi = np.array(dset['lon_{}'.format(points_type_psi)])
lat_psi = np.array(dset['lat_{}'.format(points_type_psi)])

dset.close

#---------------------------------------------------------------------
#---------------------------------------------------------------------


# load artifical bridge endpoint coordinates
file = open('artificial_coastline_insertion_points.txt','r')
bridge_point_list = file.read().splitlines()
file.close()
bridge_point_list = [ast.literal_eval(el) for el in bridge_point_list]



num_islands_intersecting = 4
coast_lon_top = []
coast_lat_top = []
coast_lon_bottom = []
coast_lat_bottom = []

bp_dex = 0

for island_number in range(1,num_islands_intersecting):   

    coastline_file_in = output_dir + 'coastline_coords_wc15_island_number_{}.p'.format(island_number)

    # Load the coastlines 
    file = open(coastline_file_in,'rb')
    coastline_lonlat = pickle.load(file)
    file.close
    coastline_lonlat = coastline_lonlat[0]


    # Handling the "top" first...
    # And just longitude, till I get it right

    #if island_number == 1:
    #    coast_lon_top += list(coastline_lonlat[0:bridge_point_list[bp_dex][0],0])
    #    bp_dex += 1
    #else:
   
    # use this to test things:
    a=[0,2,3,4]
    a[-2,:]
    etc

    if bridge_point_list[bp_dex][0] < 0:
     #   coast_lon_top += list(coastline_lonlat[bridge_point_list[bp_dex][0],0]:coastline_lonlat[bridge_point_list[bp_dex][1],0])
    
    coast_lon_top += list(coastline_lonlat[bridge_point_list[bp_dex][0],0]:coastline_lonlat[bridge_point_list[bp_dex][1],0])
    bp_dex += 1



#file = open(coastline_file_out,'wb')
#pickle.dump(coordinate_array_list,file)
#file.close()







