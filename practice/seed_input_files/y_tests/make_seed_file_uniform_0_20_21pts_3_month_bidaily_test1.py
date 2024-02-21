# Initially, just release floats at the surface.

# Later, perhaps release a fixed number for each profile from the bottom to the surface 

import time
import netCDF4
import numpy as np
import pickle
import datetime

t_0 = time.time()

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

h = np.array(dset['h'])
lon = np.array(dset['lon_rho'])
lat = np.array(dset['lat_rho'])



dset.close

points_dir = base_path + 'practice/bounding_boxes/determine_points/z_output/'
points_in_boxes_file_in = points_dir + 'points_in_boxes_lon_lat_combined.p'

seed_dir = 'practice/seed_input_files/z_output/'

runtime_text_file_pre =  'runtime_data.txt'

runtime_text_file =  seed_dir + runtime_text_file_pre
#---------------------------------------------------------------------
#---------------------------------------------------------------------

# Depth profile variables
# (currently using uniform depth profile from 0 to 20m)
profile_max_depth = 20
profile_min_depth = 0
num_per_profile = profile_max_depth-profile_min_depth + 1
#num_per_profile = int((profile_max_depth-profile_min_depth)/2) + 1

seed_file_out = 'seed_uniform_depths_{}_{}_points_per_profile_{}_3_month_bidaily_test1.txt'.format(profile_min_depth,profile_max_depth,num_per_profile)
seed_path_out = base_path + seed_dir + seed_file_out


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

#start_time = '1988-01-01 12:00:00'
#end_time = '1988-03-01 12:00:00'

start_month = 1
end_month = start_month + 2

start_time = datetime.datetime(1988,start_month,1,12,0,0)
end_time = datetime.datetime(1988,end_month,1,12,0,0)

n_days = (end_time - start_time).days

outFile = open(r'{}'.format(seed_path_out),"w")

# Set depth to 0 for now, just as a test.  Later, assign depths throughout water column
#depth = 0

# Still need to actually get a good profile at each location.  but start with 0 and -5 (should work!?)
#depths = [0,-5]
depths = list(np.linspace(-profile_max_depth, profile_min_depth, num = num_per_profile, endpoint = True))

# start with simple uniform profile

for run_day in range(0,n_days,2):
    print('time for previous day: {}'.format(round((time.time()-t_0)/3600,3)))
    for points_in_box in points_in_boxes:
        for depth in depths:
            for pp in range(np.shape(points_in_box)[1]):
                point_ij = [99999,99999]
                for ii in range(np.shape(lon)[0]): 
                    for jj in range(np.shape(lon)[1]): 
                        if lon[ii,jj] == points_in_box[0,pp] and lat[ii,jj] == points_in_box[1,pp]:
                            point_ij = [ii,jj]
                            break
                    if point_ij[0] < 10000:
                        break

                outFile.write('{}, {}, {}, {}\n'.format(points_in_box[0,pp],points_in_box[1,pp],depth,str(start_time+datetime.timedelta(days=run_day))))

outFile.close()


total_runtime = time.time()-t_0

print('seed creation runtime (hrs): {}'.format(round(total_runtime/3600,3)))

with open(runtime_text_file,"a") as out_file:
    out_file.write('seed creation runtime (hrs): {}'.format(round(total_runtime/3600,3)))





