

# Need to remove the coastal points


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


#points_type = 'psi'
points_type = 'rho'



base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

lon_grid = dset['lon_{}'.format(points_type)]

dset.close

bounding_boxes_file_in = 'bounding_boxes_ij_coords_{}_coastline_wc15_continental.p'.format(points_type)
points_in_boxes_ij_file_out = 'points_in_boxes_ij_{}.p'.format(points_type)
    
bounding_boxes_dir = 'practice/bounding_boxes/create_boxes/'
bounding_boxes_path = base_path + bounding_boxes_dir + bounding_boxes_file_in

coastline_coords_file_in = bounding_boxes_dir + 'coastline_coords_{}_file_wc15_continent.p'.format(points_type_line)



# check that these dimensions shouldn't be switched
n_i = np.shape(lon_grid)[0]    
n_j = np.shape(lon_grid)[1]
#---------------------------------------------------------------------
#---------------------------------------------------------------------



# Think I just want to grab all the (rho) i/j coordinates that fall within each
# box.  Maybe store each set in its own array within a list.  Save that, and 
# Use for seeding stuff...


# Load the boxes
file = open(bounding_boxes_path,'rb')
boxes_ij = pickle.load(file)
file.close

points_in_boxes_ij = []

# each "box" is a 2 by n array, with the first column being "i" coordinates, 2nd being "j"


# create empty list to store the combinations
points_ij = []

for ii in range(n_i):
    for jj in range(n_j):
        points_ij.append((ii,jj))

points_ij=np.array(points_ij)

# Matplotlib mplPath



for box in boxes_ij:
    if box is not None:
        path = plt_path.Path(np.transpose(box))
        points_inside_flags = path.contains_points(points_ij) 
        points_inside = points_ij[points_inside_flags]
        #points_inside = np.concatenate(points_ij[points_inside_flags], axis=0)
        #print(len(points_inside))
        
        points_box_i = []
        points_box_j = []
        for point in points_inside:
            points_box_i.append(point[0])
            points_box_j.append(point[1])
        
        points_box_ij = np.array([points_box_i,points_box_j])

        points_in_boxes_ij.append(points_inside)
        
        









file = open(points_in_boxes_ij_file_out,'wb')
pickle.dump(points_in_boxes_ij,file)
file.close()



