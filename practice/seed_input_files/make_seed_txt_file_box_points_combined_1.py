# Initially, just release floats at the surface.

# Later, perhaps release a fixed number for each profile from the bottom to the surface 


import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from random import choices





#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------


point_type_field = 'rho'
point_type_line = 'psi'


base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd.nc.0'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

h_grid = dset['h']

dset.close

points_dir = base_path + 'practice/bounding_boxes/determine_points/z_output/'
points_in_boxes_file_in_combined = points_dir + 'points_in_boxes_lon_lat_combined.p'

seed_dir = 'practice/seed_input_files/z_output/'
seed_file_out = 'box_points_seed_1.txt'
seed_path_out = base_path + seed_dir + seed_file_out

#---------------------------------------------------------------------
#---------------------------------------------------------------------


num_floats_in_profile = 10


depths_domain = np.linspace(test_point_bottom_depth,0,num_floats_in_profile)

 


# Now write the file

#format:
#-124, 35, 0, 2018-01-02 00:00:00

# I got the start time bby ust exploring variables in an early script.
# This should be ideally be obtained dynamically
start_time = '2018-01-02 00:00:00'

outFile = open(r'{}'.format(seed_path_out),"w")

for depth in float_depths_use:
    outFile.write('{}, {}, {}, {}\n'.format(test_point_lon,test_point_lat,depth,start_time))

outFile.close()


dset.close()




#plt.hist(profile_initial,bins=100,density=True)


