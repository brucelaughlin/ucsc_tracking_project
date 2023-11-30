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

file_to_change_pre = 'wc12_his_v0_Ks_tanh_'


#Ks_min = '1e-4'
#Ks_max = '1e-1'

Ks_min = '1e-3'
Ks_max = '1'


file_to_change = base_path + file_to_change_pre + Ks_min + '_' + Ks_max + '.nc'

# explore variable so i know dimensions, ie number of depth levels
dset = netCDF4.Dataset(file_to_change, 'r+')

Ks = dset['AKs']

num_levels = Ks.shape[1]

domain_step = np.pi/num_levels

domain = np.linspace(domain_step,np.pi + domain_step,num_levels)

domain_tanh = np.tanh(domain)

Ks_linear_gradient = np.linspace(float(Ks_min),float(Ks_max),num_levels)

#Ks = Ks_pre*float(Ks_max)

Ks_profile = domain_tanh * Ks_linear_gradient


plt.plot(Ks_profile)

#Ks_profile = np.linspace(float(Ks_bottom),float(Ks_top),num_levels)



# explore

#dset = netCDF4.Dataset(file_to_change, 'r')
#Ks = dset['AKs']
#Ks_profile_0 = Ks[0,:,test_point_i,test_point_j]
#plt.plot(Ks_profile_0)
#dset.close()




