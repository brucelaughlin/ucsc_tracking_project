
# diffusion:
# AKv:long_name = "vertical viscosity coefficient" ;
# Akv_bak:long_name = "background vertical mixing coefficient for momentum" ;


# velocity:
# u, ubar, v, vbar, w


import netCDF4

base_path = '/home/blaughli/tracking_project/history_files/'
file_to_change = 'wc12_his_v0_Ks_Kt_Kv_0.nc'

vars_to_zero = ['AKs','AKt','AKv']

dset = netCDF4.Dataset(base_path + file_to_change, 'r+')

for var in vars_to_zero:
    dset[var][:] = 0

dset.close()










