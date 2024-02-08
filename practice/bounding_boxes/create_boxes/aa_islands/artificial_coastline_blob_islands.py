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

#land_type = 'continent'
land_type = 'islands'

base_path = '/home/blaughli/tracking_project/'

grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])

dset.close


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
input_dir = box_dir + islands_dir + 'z_output/'

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

# First, the inshore coastline of the 4 "blob" islands
for island_number in range(1,num_islands_intersecting+1):   

    coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_number)

    # Load the coastlines 
    file = open(coastline_file_in,'rb')
    coastline_lonlat = pickle.load(file)
    file.close
    coastline_lonlat = coastline_lonlat[0]

    if bridge_point_list[island_number - 1][0] < 0:
        coast_lon_top += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:,0])
        coast_lat_top += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:,1])
        coast_lon_top += list(coastline_lonlat[0:bridge_point_list[island_number - 1][1]+1,0])
        coast_lat_top += list(coastline_lonlat[0:bridge_point_list[island_number - 1][1]+1,1])
    
    else:
        coast_lon_top += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:bridge_point_list[island_number - 1][1]+1,0])
        coast_lat_top += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:bridge_point_list[island_number - 1][1]+1,1])

coast_lonlat_top = np.column_stack([coast_lon_top,coast_lat_top])


# Now, the offshore coastline of the 4 "blob" islands
#for island_number in range(num_islands_intersecting+1,1,-1):   
for island_number in range(num_islands_intersecting,0,-1):   

    coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_number)

    # Load the coastlines 
    file = open(coastline_file_in,'rb')
    coastline_lonlat = pickle.load(file)
    file.close
    coastline_lonlat = coastline_lonlat[0]

    if bridge_point_list[island_number - 1][0] < 0:
        coast_lon_bottom += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:bridge_point_list[island_number - 1][0]+1,0])
        coast_lat_bottom += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:bridge_point_list[island_number - 1][0]+1,1])
    
    else:
        coast_lon_bottom += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:,0])
        coast_lat_bottom += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:,1])

coast_lonlat_bottom = np.column_stack([coast_lon_bottom,coast_lat_bottom])



fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")
ax.plot(coast_lonlat_top[:,0],coast_lonlat_top[:,1],c='red')
ax.plot(coast_lonlat_bottom[:,0],coast_lonlat_bottom[:,1],c='blue')
plt.show()

coast_inshore_file_out = input_dir + "coastline_coords_wc15n_island_1_through_4_combined_inshore.p"
file = open(coast_inshore_file_out,'wb')
pickle.dump(coast_lonlat_top,file)
file.close()

coast_offshore_file_out = input_dir + "coastline_coords_wc15n_island_1_through_4_combined_offshore.p"
file = open(coast_offshore_file_out,'wb')
pickle.dump(coast_lonlat_bottom,file)
file.close()






