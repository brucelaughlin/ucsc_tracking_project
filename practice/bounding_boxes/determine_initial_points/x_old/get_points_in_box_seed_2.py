

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
bounding_boxes_file_in = 'bounding_boxes_ij_coords_{}_coastline_wc15_continental.p'.format(point_type_line)
bounding_boxes_path = base_path + bounding_boxes_dir + bounding_boxes_file_in

#points_in_boxes_ij_file_out = 'points_in_boxes_ij_{}_boundary.p'.format(point_type_line)
points_in_boxes_file_out = 'points_in_boxes_lon_lat_{}_boundary.p'.format(point_type_line)    

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# something is off here - i'm getting an error bc the final box has
# a point with an "i" value of 540, which is out of bounds for psi.
# so.. what's going on?  rho has 1 extra point in each dimension...

# create interpolator to get lat/lon at isoline points
RGI = spint.RegularGridInterpolator
x = np.arange(np.shape(lon_line)[0])
y = np.arange(np.shape(lon_line)[1])
rgi_lon = RGI([x,y],lon_line)
rgi_lat = RGI([x,y],lat_line)




# Think I just want to grab all the (rho) i/j coordinates that fall within each
# box.  Maybe store each set in its own array within a list.  Save that, and 
# Use for seeding stuff...


# Load the boxes
file = open(bounding_boxes_path,'rb')
boxes_ij = pickle.load(file)
file.close

#points_in_boxes_ij = []
points_in_boxes_lon_lat = []

# create empty list to store the combinations
#points_ij = []
points_lon_lat = []

n_i = np.shape(lon_field)[0]    
n_j = np.shape(lon_field)[1]

for ii in range(n_i):
    for jj in range(n_j):
        #points_ij.append((ii,jj))
        points_lon_lat.append((lon_field[ii,jj],lat_field[ii,jj]))




#points_ij=np.array(points_ij)
points_lon_lat = np.array(points_lon_lat)

# each "box" is a 2 by n array, with the first column being "i" coordinates, 2nd being "j"

for box in boxes_ij:
    if box is not None:

        box_lat_lon = np.array([rgi_lon((box[0],box[1])),rgi_lat((box[0],box[1]))])
    
        #path = plt_path.Path(np.transpose(box))
        path = plt_path.Path(np.transpose(box_lat_lon))  # Transpose still needed?
        
        #points_inside_flags = path.contains_points(points_ij) 
        points_inside_flags = path.contains_points(points_lon_lat) 
        
        #points_inside = points_ij[points_inside_flags]
        points_inside = points_lon_lat[points_inside_flags]
        
       # points_box_i = []
       # points_box_j = []
       # for point in points_inside:
       #     points_box_i.append(point[0])
       #     points_box_j.append(point[1])
        
        points_box_lon = []
        points_box_lat = []
        for point in points_inside:
            points_box_lon.append(point[0])
            points_box_lat.append(point[1])
        
        #points_box_ij = np.array([points_box_i,points_box_j])
        points_box_lon_lat = np.array([points_box_lon,points_box_lat])

        #points_in_boxes_ij.append(points_inside) # ???? did I mess this up????
        #points_in_boxes_ij.append(points_box_ij)
        points_in_boxes_lon_lat.append(points_box_lon_lat)
        
        







file = open(points_in_boxes_file_out,'wb')
#pickle.dump(points_in_boxes_ij,file)
pickle.dump(points_in_boxes_lon_lat,file)
file.close()


#file = open(points_in_boxes_ij_file_out,'wb')
#pickle.dump(points_in_boxes_ij,file)
#file.close()



