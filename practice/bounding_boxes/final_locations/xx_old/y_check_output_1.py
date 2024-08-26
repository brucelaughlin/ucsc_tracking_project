# ncview not showing anything... what's going on?
# Perhaps a problem is that I don't have an "opendrift" environment on the nodes?

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join


output_dir = '/data03/blaughli/tracking_project_output/test2_physics_only/'
output_files = [f for f in listdir(output_dir) if isfile(join(output_dir,f))]
output_files.sort()

print(output_files[0])



#test_file = output_dir + sample_output_file

#dset = netCDF4.Dataset(test_file, 'r')
#NO3 = np.array(dset['NO3'])
#lat = np.array(dset['lat'])
#lon = np.array(dset['lon'])
#z = np.array(dset['z'])
#status = np.array(dset['status'])
#dset.close

#particle_id = 100000
#test_no3 = NO3[particle_id,20:100]

#test_no3 = NO3[particle_id,:]

#test_status = status[particle_id,:]

#good_indices = test_status == 0

#test_no3 = NO3[particle_id,good_indices]


#fig,ax = plt.subplots()

#ax.plot(test_no3)

#ax.plot(test_status)
#ax.plot(test_status[20:100])
#ax.plot(test_status[0:10])

