
# MODIFY THIS BEFORE CREATING NEW SEED FILE - 
profile_shape_name = 'line_slope1'





# example entry, from my original test efforts
# -123.9, 35.1, -150, 2018-01-02 00:00:00
# let's try using the i=113, j=73 horizontal coordinate in the history files 

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from random import choices






base_path = '/home/blaughli/tracking_project/'

his_directory = 'history_files/'
seed_directory = '/practice/seed_input_files/'

his_file_in = 'wc12_his_dummy_zeros.nc'
seed_file_out = 'seed_turbulence_test_psi_{}.txt'.format(profile_shape_name)

his_path_in = base_path + his_directory + his_file_in
seed_path_out = base_path + seed_directory + seed_file_out

dset = netCDF4.Dataset(his_path_in, 'r')


# position variables I'll use:
# lon_rho, lat_rho, h

h_grid = dset['h']
rho_lon_grid = dset['lon_rho']
rho_lat_grid = dset['lat_rho']



# grid indices of test rho point, hopefully close to bodega bay
# (chosen by eye using ncview)

test_point_i = 133
test_point_j = 73

test_point_lon = rho_lon_grid[test_point_i,test_point_j]
test_point_lat = rho_lat_grid[test_point_i,test_point_j]
test_point_bottom_depth = -1*h_grid[test_point_i,test_point_j]

num_floats = int(1e3)

#depths_domain = np.linspace(test_point_bottom_depth,0,num_floats)


# re-write this to make your own pdf from a profile curve of your choice
# also do this for diffusivity

# psi pdf 1: line 
# wait, grabbing from pdf is dumb, since the depth domain is discrete.  so
# if 2 floats are placed at the same depth, they'll just do the exact same 
# thing as each other.  So... really what we want is a modification of
# the depths chosen themselves, to allow finer selection where the pdf
# has more probability


#depths_domain = np.linspace(test_point_bottom_depth,0,num_floats*int(1e3))
#depths_domain = np.linspace(test_point_bottom_depth,0,np.power(num_floats,3))

domain_resolution_boost_factor = int(1e4)
depths_domain = np.linspace(test_point_bottom_depth,0,num_floats*domain_resolution_boost_factor)

 
domain_size = len(depths_domain)
    
slope = 1


# To determine the fomula of the pdf for the profile i want, i had to draw
# it correctly and then solve for its parameters.  see note picture.  
# was basically a line sloping up, with # of floats on the y axis and
# depth on the x axis.  had to solve for the intercept.

pdf_curve = slope*depths_domain - slope*test_point_bottom_depth

depth_weights = pdf_curve/np.sum(pdf_curve)

float_depths_sampled = choices(depths_domain, depth_weights, k=num_floats)


#plt.hist(float_depths_sampled,bins=100,density=True)
#plt.show()

float_depths_use = np.unique(float_depths_sampled)


# experiment with various pdfs of initial depths
# start with fixed (this is different than uniform, right?)





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


