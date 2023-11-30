# Set AKs at the test point to be a tanh profile

import netCDF4
import scipy.io
from scipy.interpolate import interp1d
import numpy as np

test_point_i = 133
test_point_j = 73

depths_w_file = '/home/blaughli/tracking_project/grid_data/depths_w.mat'
depths_w = scipy.io.loadmat(depths_w_file)
depths_w = depths_w['depths_w']
depths_w_profile = depths_w[test_point_i,test_point_j,:]
num_levels = np.shape(depths_w_profile)[0]

Ks_bottom = '1e-3'
Ks_top = '1e-1'
Ks_domain = [float(Ks_bottom),float(Ks_top)]
depths_domain = [min(depths_w_profile),max(depths_w_profile)]
f = interp1d(depths_domain, Ks_domain)
Ks_w_profile = f(depths_w_profile)

radian_resolution = 1000
radian_step = np.pi/radian_resolution
radian_domain = np.linspace(radian_step,np.pi + radian_step,radian_resolution)
domain_tanh = np.tanh(radian_domain)
domain_Ks = domain_tanh * float(Ks_top)
domain_depths = np.linspace(min(depths_w_profile),max(depths_w_profile),radian_resolution)
f = interp1d(domain_depths,domain_Ks)
Ks_profile = f(depths_w_profile)

base_path = '/home/blaughli/tracking_project/history_files/'
file_to_change_pre = 'wc12_his_v0_Ks_tanh_'
file_to_change = base_path + file_to_change_pre + Ks_top + '.nc'

dset = netCDF4.Dataset(file_to_change, 'r+')
Ks = dset['AKs']

for tt in range(Ks.shape[0]):
    Ks[tt,:,test_point_i,test_point_j] = Ks_profile

dset.close()