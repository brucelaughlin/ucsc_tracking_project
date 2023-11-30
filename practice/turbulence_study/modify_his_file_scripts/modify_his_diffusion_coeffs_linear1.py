# looking at ncks -m wc12_his.nc, looking for diffusion coefficients and also velocity variables.


# diffusion:
#
# ACTUALLY::::::
# Chris is guessing that floats should act "more like salt ions"
# than "heat or momentum", so his guess is that AKs is read by opendrift,
# rather that AKv.  BUT, try Ks, AKt, and AKv, just to see what happens...
#




import netCDF4
import numpy as np
import matplotlib.pyplot as plt



test_point_i = 133
test_point_j = 73



base_path = '/home/blaughli/tracking_project/history_files/'

file_to_change_pre = 'wc12_his_v0_Ks_linear_'


Ks_bottom = '1e-4'
Ks_top = '1e-1'

file_to_change = base_path + file_to_change_pre + Ks_bottom + '_' + Ks_top + '.nc'

# explore variable so i know dimensions, ie number of depth levels
dset = netCDF4.Dataset(file_to_change, 'r+')

Ks = dset['AKs']

num_levels = Ks.shape[1]

Ks_profile = np.linspace(float(Ks_bottom),float(Ks_top),num_levels)

for tt in range(Ks.shape[0]):
    Ks[tt,:,test_point_i,test_point_j] = Ks_profile


dset.close()



# explore

#dset = netCDF4.Dataset(file_to_change, 'r')
#Ks = dset['AKs']
#Ks_profile_0 = Ks[0,:,test_point_i,test_point_j]
#plt.plot(Ks_profile_0)
#dset.close()




