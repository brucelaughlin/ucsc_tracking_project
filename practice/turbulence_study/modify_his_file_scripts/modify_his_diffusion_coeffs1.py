# looking at ncks -m wc12_his.nc, looking for diffusion coefficients and also velocity variables.


# diffusion:
#
# ACTUALLY::::::
# Chris is guessing that floats should act "more like salt ions"
# than "heat or momentum", so his guess is that AKs is read by opendrift,
# rather that Akv.  BUT, try AKs, AKt, and AKv, just to see what happens...
#




import netCDF4

base_path = '/home/blaughli/tracking_project/history_files/'

file_to_change_pre = 'wc12_his_v0_Ks_'

var_to_change = 'AKs'

var_values = ['1e-1','1e-2','1e-3','1e-4']

for ii in range(0,4):

    dset = netCDF4.Dataset(base_path + file_to_change_pre + var_values[ii] + '.nc', 'r+')
    dset[var_to_change][:] = float(var_values[ii])
    dset.close()










