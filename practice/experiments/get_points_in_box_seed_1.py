

import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint

import itertools
from itertools import permutations 

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

bounding_boxes_file_in = 'bounding_boxes_ij_coords_{}_coastline_wc15_continental.p'.format(points_type)
points_in_boxes_ij_file_out = 'points_in_boxes_ij_{}.p'.format(points_type)
    


lon_grid = dset['lon_{}'.format(points_type)]

# check that these dimensions shouldn't be switched
n_i = np.shape(lon_grid)[0]    
n_j = np.shape(lon_grid)[1]
#---------------------------------------------------------------------
#---------------------------------------------------------------------



# Think I just want to grab all the (rho) i/j coordinates that fall within each
# box.  Maybe store each set in its own array within a list.  Save that, and 
# Use for seeding stuff...


# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_ij = pickle.load(file)
file.close

points_in_boxes_ij = []

# each "box" is a 2 by n array, with the first column being "i" coordinates, 2nd being "j"

list_i = range(n_i)
list_j = range(n_j)

# Getting all permutations of list_i
# with length of list_j
permut = itertools.permutations(list_i, len(list_j))
 

# ----- FINISH -------

# https://www.geeksforgeeks.org/python-program-to-get-all-unique-combinations-of-two-lists/

# zip() is called to pair each permutation
# and shorter list element into combination
for comb in permut:
    zipped = zip(comb, list_2)
    unique_combinations.append(list(zipped))



# Matplotlib mplPath
path = mpltPath.Path(polygon)
inside2 = path.contains_points(points)


for box in boxes_ij:
    if box is not None:
        for ii in range(n_i):    
            for jj in range(n_j):    
                if 
                

        ax.plot(box[1],box[0])








file = open(bounding_boxes_file_out,'wb')
pickle.dump(points_in_boxes_ij,file)
file.close()



