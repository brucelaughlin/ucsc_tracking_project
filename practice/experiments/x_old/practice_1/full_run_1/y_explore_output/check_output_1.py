# ncview not showing anything... what's going on?
# Perhaps a problem is that I don't have an "opendrift" environment on the nodes?

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join

#output_dir = '/data03/blaughli/tracking_project_output/test1/'
#sample_output_file = 'tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_20_startNudge_000.nc'
output_dir = '/data03/blaughli/tracking_project_output/test2_physics_only/'
sample_output_file = 'tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_020_startNudge_000000.nc'

tracking_output_files = [f for f in listdir(output_dir) if isfile(join(output_dir,f))]
tracking_output_files.sort()

sample_output_file = tracking_output_files[1]

test_file = output_dir + sample_output_file

dset = netCDF4.Dataset(test_file, 'r')
NO3 = np.array(dset['NO3'])
#lat = np.array(dset['lat'])
#lon = np.array(dset['lon'])
#z = np.array(dset['z'])
status = np.array(dset['status'])
trajectory = np.array(dset['trajectory'])
dset.close

particle_id = 100000
test_no3 = NO3[particle_id,20:100]
#test_no3 = NO3[particle_id,:]

test_status = status[particle_id,:]

good_indices = test_status == 0

test_no3 = NO3[particle_id,good_indices]


mask_field = status == 0

#masked_no3 = NO3[mask_field]
masked_no3 = np.where(mask_field, NO3, 0)

i_dim = np.shape(NO3)[0]
j_dim = np.shape(NO3)[1]

X = np.arange(-0.5,i_dim,1)
Y = np.arange(-0.5,j_dim,1)

#print(test_status[50])

fig,ax = plt.subplots()

#ax.pcolormesh(X,Y,masked_no3)
#ax.pcolormesh(masked_no3)
ax.pcolormesh(NO3)

#ax.plot(trajectory)
#ax.plot(test_status)

#ax.plot(test_no3)
#ax.plot(test_no3)
#ax.plot(test_status[20:100])
#ax.plot(test_status[0:10])

plt.show()

