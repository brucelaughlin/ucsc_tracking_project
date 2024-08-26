# V2: New idea: insert a point halfway along each artificial bridge, and later use ONLY those 
# as the coastline boundaries of the boxes - ie draw all cross-shore walls starting at one
# of these points, so walls only start in the middle of bridges.  Actually, for the 
# first an last islands in the blob, also have a point at the far side in the middle.  THEN,
# each island will have a north and south box, and no boxes will span two islands.  Boxes might
# be bigger/smaller than 300km*^2 but I'm guessing this is fine.

# Load the coastlines for the "blob" islands and insert artifical 1-D "bridges" between them,
# to be used for defining boxes

# Wait.... since we want an "north" and "south" side of each island, perhaps, for the blobs,
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
islands_dir = 'modify_islands/'
#islands_dir = 'aa_islands/'
input_dir = box_dir + islands_dir + 'z_output/'

#---------------------------------------------------------------------
#---------------------------------------------------------------------


# load artifical bridge endpoint coordinates
file = open('artificial_coastline_insertion_points.txt','r')
bridge_point_list = file.read().splitlines()
file.close()
bridge_point_list = [ast.literal_eval(el) for el in bridge_point_list]


num_islands_intersecting = 4
coast_lon_north = []
coast_lat_north = []
coast_lon_south = []
coast_lat_south = []

# ------------------------------------------------------------
# Mods to control the box positions
# ------------------------------------------------------------
forced_box_north_endpoints = []
forced_box_south_endpoints = []
bridge_mid_points_lon = []
bridge_mid_points_lat = []
# ------------------------------------------------------------
first_point_switch = True
# ------------------------------------------------------------


# First, the north coastline of the 4 "blob" islands
for island_number in range(1,num_islands_intersecting+1):   

    coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_number)

    # Load the coastlines 
    file = open(coastline_file_in,'rb')
    coastline_lonlat = pickle.load(file)
    file.close
    coastline_lonlat = coastline_lonlat[0]

    if first_point_switch:
        forced_box_north_endpoints.append(0)        
        first_point_switch = False

    if bridge_point_list[island_number - 1][0] < 0:
        coast_lon_north += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:,0])
        coast_lat_north += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:,1])
        coast_lon_north += list(coastline_lonlat[0:bridge_point_list[island_number - 1][1]+1,0])
        coast_lat_north += list(coastline_lonlat[0:bridge_point_list[island_number - 1][1]+1,1])
   
    else:
        coast_lon_north += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:bridge_point_list[island_number - 1][1]+1,0])
        coast_lat_north += list(coastline_lonlat[bridge_point_list[island_number - 1][0]:bridge_point_list[island_number - 1][1]+1,1])

    # Add the new point in the middle of the bridge
    if island_number < num_islands_intersecting :
        coast_lon_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1],0] + coastline_lonlat[bridge_point_list[island_number][0],0])/2.0)
        coast_lat_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1],1] + coastline_lonlat[bridge_point_list[island_number][0],1])/2.0)
       
        print(island_number)
        print("lon,lat:")
        print("{}, {}",coastline_lonlat[bridge_point_list[island_number - 1][1],0],coastline_lonlat[bridge_point_list[island_number - 1][1],1])
        print("{}, {}",coastline_lonlat[bridge_point_list[island_number][1],0],coastline_lonlat[bridge_point_list[island_number][1],1])
        

        #coast_lon_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1]+1,0] + coastline_lonlat[bridge_point_list[island_number][0]+1,0])/2.0)
        #coast_lat_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1]+1,1] + coastline_lonlat[bridge_point_list[island_number][0]+1,1])/2.0)
        
        #coast_lon_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1]+1,0] + coastline_lonlat[bridge_point_list[island_number][1]+1,0])/2.0)
        #coast_lat_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1]+1,1] + coastline_lonlat[bridge_point_list[island_number][1]+1,1])/2.0)
        
        
        #coast_lat_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1]+1,0] + coastline_lonlat[bridge_point_list[island_number][1]+1,1])/2.0)
        
        #coast_lon_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1]+1,0] + bridge_point_list[island_number][1]+1,0])/2.0)
        #coast_lat_north.append((coastline_lonlat[bridge_point_list[island_number - 1][1]+1,0] + bridge_point_list[island_number][1]+1,1])/2.0)
        
        bridge_mid_points_lon.append(coast_lon_north[-1])
        bridge_mid_points_lat.append(coast_lat_north[-1])

    # record the index of the added mid-bridge point, for later indexing
    forced_box_north_endpoints.append(len(coast_lon_north)-1)
        
coast_lonlat_north = np.column_stack([coast_lon_north,coast_lat_north])


# ------------------------------------------------------------
first_point_switch = True
# ------------------------------------------------------------

# Now, the south coastline of the 4 "blob" islands
#for island_number in range(num_islands_intersecting+1,1,-1):   
for island_number in range(num_islands_intersecting,0,-1):   

    coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_number)

    # Load the coastlines 
    file = open(coastline_file_in,'rb')
    coastline_lonlat = pickle.load(file)
    file.close
    coastline_lonlat = coastline_lonlat[0]

    if first_point_switch:
        forced_box_south_endpoints.append(0)        
        first_point_switch = False

    if bridge_point_list[island_number - 1][0] < 0:
        coast_lon_south += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:bridge_point_list[island_number - 1][0]+1,0])
        coast_lat_south += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:bridge_point_list[island_number - 1][0]+1,1])
    
    else:
        coast_lon_south += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:,0])
        coast_lat_south += list(coastline_lonlat[bridge_point_list[island_number - 1][1]:,1])
    
    # Add the new point in the middle of the bridge
    if island_number >  1 :
        coast_lon_south.append(bridge_mid_points_lon.pop())
        coast_lat_south.append(bridge_mid_points_lat.pop())
       
    # record the index of the added mid-bridge point, for later indexing
    forced_box_north_endpoints.append(len(coast_lon_north)-1)


coast_lonlat_south = np.column_stack([coast_lon_south,coast_lat_south])



fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")
ax.plot(coast_lonlat_north[:,0],coast_lonlat_north[:,1],c='red')
#ax.plot(coast_lonlat_south[:,0],coast_lonlat_south[:,1],c='blue')
plt.show()

coast_north_file_out = input_dir + "coastline_coords_wc15n_island_1_through_4_combined_north.p"
file = open(coast_north_file_out,'wb')
pickle.dump(coast_lonlat_north,file)
file.close()

coast_south_file_out = input_dir + "coastline_coords_wc15n_island_1_through_4_combined_south.p"
file = open(coast_south_file_out,'wb')
pickle.dump(coast_lonlat_south,file)
file.close()






