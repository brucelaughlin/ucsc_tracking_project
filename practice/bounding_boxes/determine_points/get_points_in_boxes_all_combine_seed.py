# Now that I'm doing everything in Lat/Lon from the get-go, I don't think I need
# any of this interpolation business...

# Need to remove the coastal points

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


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
continent_dir = 'continent/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + continent_dir + 'z_output/'


points_in_boxes_file_out_continent = 'z_output/' + 'points_in_boxes_lon_lat_continent.p'
points_in_boxes_file_out_islands_offshore = 'z_output/' + 'points_in_boxes_lon_lat_islands_offshore.p'
points_in_boxes_file_out_islands_inshore = 'z_output/' + 'points_in_boxes_lon_lat_islands_inshore.p'

points_in_boxes_file_out_combined = 'z_output/' + 'points_in_boxes_lon_lat_combined.p'


#---------------------------------------------------------------------
#---------------------------------------------------------------------

# Think I just want to grab all the (rho) lat/lon coordinates that fall within each
# box.  Maybe store each set in its own array within a list.  Save that, and 
# Use for seeding stuff...



# create empty list to store all of the grid lat/lon pairs as tuples
points_lon_lat = []

n_i = np.shape(lon_field)[0]    
n_j = np.shape(lon_field)[1]

for ii in range(n_i):
    for jj in range(n_j):
        #points_ij.append((ii,jj))
        points_lon_lat.append((lon_field[ii,jj],lat_field[ii,jj]))


points_lon_lat = np.array(points_lon_lat)



# Continent


bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(point_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

points_in_boxes_lonlat_continent = []

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
        
        points_inside_flags = path.contains_points(points_lon_lat) 
        
        points_inside = points_lon_lat[points_inside_flags]
        
        points_box_lon = []
        points_box_lat = []
        for point in points_inside:
            points_box_lon.append(point[0])
            points_box_lat.append(point[1])
        
        points_box_lon_lat = np.array([points_box_lon,points_box_lat])

        points_in_boxes_lonlat_continent.append(points_box_lon_lat)
        



# Islands

points_in_boxes_lonlat_islands_inshore = []
points_in_boxes_lonlat_islands_offshore = []

num_islands = 8
num_last_blob_island = 4


for island_dex in range(num_last_blob_island,num_islands+1):
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):

    # Set an index for the bounding point lists (the lists of points used to split the coastlines and isolines)
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

                #box_lonlat = np.array([rgi_lon((box[0],box[1])),rgi_lat((box[0],box[1]))])
            
                path = plt_path.Path(np.transpose(box_lonlat))  # Transpose still needed?
                
                points_inside_flags = path.contains_points(points_lon_lat) 
                
                points_inside = points_lon_lat[points_inside_flags]
                
                points_box_lon = []
                points_box_lat = []
                for point in points_inside:
                    points_box_lon.append(point[0])
                    points_box_lat.append(point[1])
                
                points_box_lon_lat = np.array([points_box_lon,points_box_lat])

            
                if inoffshore_switch == 0:
                    points_in_boxes_lonlat_islands_inshore.append(points_box_lon_lat)
                else:
                    points_in_boxes_lonlat_islands_offshore.append(points_box_lon_lat)





file = open(points_in_boxes_file_out_continent,'wb')
pickle.dump(points_in_boxes_lonlat_continent,file)
file.close()

file = open(points_in_boxes_file_out_islands_inshore,'wb')
pickle.dump(points_in_boxes_lonlat_islands_inshore,file)
file.close()


file = open(points_in_boxes_file_out_islands_offshore,'wb')
pickle.dump(points_in_boxes_lonlat_islands_offshore,file)
file.close()


# Store all seed points in a single list, for use in making a seed file

points_in_boxes_lonlat_combined = points_in_boxes_lonlat_continent + points_in_boxes_lonlat_islands_inshore + points_in_boxes_lonlat_islands_offshore

file = open(points_in_boxes_file_out_combined,'wb')
pickle.dump(points_in_boxes_lonlat_combined,file)
file.close()




