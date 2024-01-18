

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
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

lon_field = np.array(dset['lon_{}'.format(point_type_field)])
lat_field = np.array(dset['lat_{}'.format(point_type_field)])
lon_line = np.array(dset['lon_{}'.format(point_type_line)])
lat_line = np.array(dset['lat_{}'.format(point_type_line)])

dset.close

bounding_boxes_dir = 'practice/bounding_boxes/create_boxes/'
bounding_boxes_file_in = 'bounding_boxes_lonlat_coords_{}_coastline_wc15_continental.p'.format(point_type_line)
bounding_boxes_path = base_path + bounding_boxes_dir + bounding_boxes_file_in


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + 'z_output/'


points_in_boxes_file_out = 'points_in_boxes_all_lon_lat.p'



#---------------------------------------------------------------------
#---------------------------------------------------------------------

# something is off here - i'm getting an error bc the final box has
# a point with an "i" value of 540, which is out of bounds for psi.
# so.. what's going on?  rho has 1 extra point in each dimension...

# Create interpolator to get lat/lon at isoline points
#
# Note: I'm "naively" using the psi grid for this, since I defined the coast along
# psi points...
RGI = spint.RegularGridInterpolator
x = np.arange(np.shape(lon_line)[0])
y = np.arange(np.shape(lon_line)[1])
rgi_lon = RGI([x,y],lon_line)
rgi_lat = RGI([x,y],lat_line)




# Think I just want to grab all the (rho) i/j coordinates that fall within each
# box.  Maybe store each set in its own array within a list.  Save that, and 
# Use for seeding stuff...



# create empty list to store the combinations
#points_ij = []
points_lon_lat = []

n_i = np.shape(lon_field)[0]    
n_j = np.shape(lon_field)[1]

for ii in range(n_i):
    for jj in range(n_j):
        #points_ij.append((ii,jj))
        points_lon_lat.append((lon_field[ii,jj],lat_field[ii,jj]))


points_lon_lat = np.array(points_lon_lat)



# Continent


bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15_continental.p'.format(point_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

points_in_boxes_lonlat = []

# each "box" is a 2 by n array, with the first column being "i" coordinates, 2nd being "j"

box_dex = 0

#for box in boxes_lonlat:
for ii in range(3,len(boxes_lonlat)-3):
    box = boxes_lonlat[ii]
    box_dex += 1
    if box is not None:

        box_lat_lon = np.array([rgi_lon((box[0,:],box[1,:])),rgi_lat((box[0,:],box[1,:]))])
    
        path = plt_path.Path(np.transpose(box_lat_lon))  # Transpose still needed?
        
        points_inside_flags = path.contains_points(points_lon_lat) 
        
        points_inside = points_lon_lat[points_inside_flags]
        
        points_box_lon = []
        points_box_lat = []
        for point in points_inside:
            points_box_lon.append(point[0])
            points_box_lat.append(point[1])
        
        points_box_lon_lat = np.array([points_box_lon,points_box_lat])

        points_in_boxes_lonlat.append(points_box_lon_lat)
        



# Islands

num_islands = 8
num_last_blob_island = 4


for island_dex in range(num_last_blob_island,num_islands+1):
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):

    # Set an index for the bounding point lists (the lists of points used to split the coastlines and isolines)
    bp_dex = island_dex-num_last_blob_island

    for inoffshore_switch in range(0,2):


        if inoffshore_switch == 0:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15_island_number_{}_offshore.p'.format(island_dex)


        # Load the boxes
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close        


        for box in boxes_lonlat:
            if box is not None:

                #box_lat_lon = np.array([rgi_lon((box[0],box[1])),rgi_lat((box[0],box[1]))])
                box_lat_lon = np.array([rgi_lon((box[0,:],box[1,:])),rgi_lat((box[0,:],box[1,:]))])
            
                path = plt_path.Path(np.transpose(box_lat_lon))  # Transpose still needed?
                
                points_inside_flags = path.contains_points(points_lon_lat) 
                
                points_inside = points_lon_lat[points_inside_flags]
                
                points_box_lon = []
                points_box_lat = []
                for point in points_inside:
                    points_box_lon.append(point[0])
                    points_box_lat.append(point[1])
                
                points_box_lon_lat = np.array([points_box_lon,points_box_lat])

                points_in_boxes_lonlat.append(points_box_lon_lat)





file = open(points_in_boxes_file_out,'wb')
#pickle.dump(points_in_boxes_lonlat,file)
pickle.dump(points_in_boxes_lonlat,file)
file.close()


#file = open(points_in_boxes_lonlat_file_out,'wb')
#pickle.dump(points_in_boxes_lonlat,file)
#file.close()



