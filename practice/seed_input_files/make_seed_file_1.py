

# example entry, from my original test efforts

# -123.9, 35.1, -150, 2018-01-02 00:00:00



# Plan (without input from Chris yet): before proceeding further,
# write script that will store all of the i,j coordinates of 
# the rho points within each of the bounding boxes.  Then just 
# seed from all of those.  Will want to know which box the 
# particles started in for statistics, so make sure to store that,
# not just one big list of rho points shoreward of an isoline boundary.



import netCDF4
import numpy as np
import matplotlib.pyplot as plt


#-------------------- EDIT THESE If NECESSARY-------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')


h_grid = np.array(dset['h'])
lon_grid = np.array(dset['lon_rho'])
lat_grid = np.array(dset['lat_rho'])

dset.close()
#---------------------------------------------------------------------
#---------------------------------------------------------------------




# position variables I'll use:
# lon_rho, lat_rho, h




# grid indices of test rho point, hopefully close to bodega bay
# (chosen by eye using ncview)

test_point_i = 133
test_point_j = 73

test_point_lon = lon_grid[test_point_i,test_point_j]
test_point_lat = lat_grid[test_point_i,test_point_j]
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


