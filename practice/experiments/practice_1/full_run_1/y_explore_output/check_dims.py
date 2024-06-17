# ncview not showing anything... what's going on?
# Perhaps a problem is that I don't have an "opendrift" environment on the nodes?

import netCDF4
import matplotlib.pyplot as plt
import numpy as np

#output_dir = '/data03/blaughli/tracking_project_output/test1/'
#sample_output_file = 'tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_20_startNudge_000.nc'
output_dir = '/data03/blaughli/tracking_project_output/test2_physics_only/'
sample_output_file = 'tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_020_startNudge_000000.nc'

test_file = output_dir + sample_output_file

dset = netCDF4.Dataset(test_file, 'r')
NO3 = np.array(dset['NO3'])
#lat = np.array(dset['lat'])
#lon = np.array(dset['lon'])
#z = np.array(dset['z'])
status = np.array(dset['status'])
trajectory = np.array(dset['trajectory'])
dset.close


