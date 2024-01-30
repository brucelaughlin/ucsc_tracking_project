# Make two sets of floats, separated by an hour

import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl




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

h = np.array(dset['h'])
lon = np.array(dset['lon_rho'])
lat = np.array(dset['lat_rho'])



dset.close

points_dir = base_path + 'practice/bounding_boxes/determine_points/z_output/'
points_in_boxes_file_in = points_dir + 'points_in_boxes_lon_lat_combined.p'


seed_file_out_1 = 'box_points_seed_2_hours_1.txt'
seed_file_out_2 = 'box_points_seed_2_hours_2.txt'

seed_dir = 'practice/seed_input_files/z_output/'
seed_path_out_1 = base_path + seed_dir + seed_file_out_1
seed_path_out_2 = base_path + seed_dir + seed_file_out_2


#---------------------------------------------------------------------
#---------------------------------------------------------------------

file = open(points_in_boxes_file_in,'rb')
points_in_boxes= pickle.load(file)
file.close





#num_floats_in_profile = 10

#depths_domain = np.linspace(test_point_bottom_depth,0,num_floats_in_profile)

 


# Now write the file

#format:
#-124, 35, 0, 2018-01-02 00:00:00

# I got the start time bby ust exploring variables in an early script.
# This should be ideally be obtained dynamically

# Jerome's daily output has a single timestamp, at hour 12 of the given day

start_time_1 = '1988-01-01 12:00:00'
start_time_2 = '1988-01-01 13:00:00'


out_file_1 = open(r'{}'.format(seed_path_out_1),"w")
out_file_2 = open(r'{}'.format(seed_path_out_2),"w")

# Set depth to 0 for now, just as a test.  Later, assign depths throughout water column
#depth = 0

# Still need to actually get a good profile at each location.  but start with 0 and -5 (should work!?)
#depths = [0,-5]

# start with simple uniform profile
num_depths_constant = 5


for points_in_box in points_in_boxes:


    #for point in points_in_box:
    for pp in range(np.shape(points_in_box)[1]):

        point_ij = [99999,99999]

        for ii in range(np.shape(lon)[0]): 
            for jj in range(np.shape(lon)[1]): 
                #if lon_filtered[ii,jj] == True and lat_filtered[ii,jj
                if lon[ii,jj] == points_in_box[0,pp] and lat[ii,jj] == points_in_box[1,pp]:

                    point_ij = [ii,jj]
                    #h_point = h[ii,jj]
                    break
            if point_ij[0] < 10000:
                break

        h_point = h[point_ij[0],point_ij[1]]
    
        depth_profile = np.linspace(-1 * h_point, 0 ,num_depths_constant)

        for depth in depth_profile:

            out_file_1.write('{}, {}, {}, {}\n'.format(points_in_box[0,pp],points_in_box[1,pp],depth,start_time_1))
            out_file_2.write('{}, {}, {}, {}\n'.format(points_in_box[0,pp],points_in_box[1,pp],depth,start_time_2))



out_file_1.close()
out_file_2.close()








