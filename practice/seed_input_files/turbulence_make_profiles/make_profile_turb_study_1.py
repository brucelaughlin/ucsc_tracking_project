

# example entry, from my original test efforts

# -123.9, 35.1, -150, 2018-01-02 00:00:00

# let's try using the i=113, j=73 horizontal coordinate in the history files 



import netCDF4
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'

his_directory = 'history_files/'
seed_directory = '/practice/seed_input_files/'

his_file_in = 'wc12_his_dummy_zeros.nc'
seed_file_out = 'seed_turbulence_test1.txt'

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



# experiment with various pdfs of initial depths
# start with fixed (this is different than uniform, right?)

profile_initial = np.linspace(test_point_bottom_depth,0,num_floats)



# Now write the file

#format:
#-124, 35, 0, 2018-01-02 00:00:00

# I got the start time bby ust exploring variables in an early script.
# This should be ideally be obtained dynamically
start_time = '2018-01-02 00:00:00'

outFile = open(r'{}'.format(seed_path_out),"w")

for depth in profile_initial:
    outFile.write('{}, {}, {}, {}\n'.format(test_point_lon,test_point_lat,depth,start_time))

outFile.close()


dset.close()




#plt.hist(profile_initial,bins=100,density=True)


