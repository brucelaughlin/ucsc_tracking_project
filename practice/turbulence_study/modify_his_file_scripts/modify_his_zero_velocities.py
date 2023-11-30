# looking at ncks -m wc12_his.nc, looking for diffusion coefficients and also velocity variables.


# diffusion:
# AKv:long_name = "vertical viscosity coefficient" ;
# Akv_bak:long_name = "background vertical mixing coefficient for momentum" ;


# velocity:
# u, ubar, v, vbar, w


import netCDF4

base_path = '/home/blaughli/tracking_project/history_files/'
file_to_change = 'wc12_his_dummy_zeros.nc'

vars_to_zero = ['u','ubar','v','vbar','w']

dset = netCDF4.Dataset(base_path + file_to_change, 'r+')

for var in vars_to_zero:
    dset[var][:] = 0

dset.close()










