# looking at ncks -m wc12_his.nc, looking for diffusion coefficients and also velocity variables.


# diffusion:
#
# ACTUALLY::::::
# Chris is guessing that floats should act "more like salt ions"
# than "heat or momentum", so his guess is that AKs is read by opendrift,
# rather that AKv.  BUT, try Ks, AKt, and AKv, just to see what happens...
#

import netCDF4
import scipy.io
from scipy.interpolate import interp1d

test_point_i = 133
test_point_j = 73

depths_rho_file = '/home/blaughli/tracking_project/grid_data/depths_rho.mat'
depths_rho = scipy.io.loadmat(depths_rho_file)
depths_rho = depths_rho['depths_rho']
depths_rho_profile = depths_rho[test_point_i,test_point_j,:]

Ks_bottom = '1e-2'
Ks_top = '1e-1'
Ks_domain = [float(Ks_bottom),float(Ks_top)]
depths_domain = [min(depths_rho_profile),max(depths_rho_profile)]
f = interp1d(depths_domain, Ks_domain)
Ks_rho_profile = f(depths_rho_profile)

# =============================================================================
# import matplotlib.pyplot as plt
# plt.plot(Ks_rho_profile)
# plt.title('Ks vs Sigma level')
# plt.plot(depths_rho_profile,Ks_rho_profile)
# plt.title('Ks vs depth')
# =============================================================================

base_path_his = '/home/blaughli/tracking_project/history_files/'
file_to_change_pre = 'wc12_his_v0_Ks_linear_'
file_to_change = base_path_his + file_to_change_pre + Ks_bottom + '_' + Ks_top + '.nc'

# Now change the history file AKs values
dset = netCDF4.Dataset(file_to_change, 'r+')
Ks = dset['AKs']

for tt in range(Ks.shape[0]):
    Ks[tt,:,test_point_i,test_point_j] = Ks_rho_profile


dset.close()