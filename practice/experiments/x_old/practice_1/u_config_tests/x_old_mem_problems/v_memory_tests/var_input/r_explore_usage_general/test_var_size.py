

import numpy as np
import netCDF4
import os

# copied from https://pastebin.com/TBhs0Dcd
def get_used_mem():
    # Quick and dirty memory check with `free`,
    # without having to install e.g. psutil
    return int(os.popen('free -m').readlines()[1].split()[2])

mem0 = get_used_mem()


#export_variables_list = ['z','sea_water_temperature','sea_water_salinity','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']
variables_list = ['temp','salt','CalC','DON','NH4','NO3','PON','Pzooplankton','SiOH4','TIC','alkalinity','diatom','mesozooplankton','microzooplankton','nanophytoplankton','omega','opal','oxygen','pCO2','pH']

base_path = '/home/blaughli/tracking_project/'

history_base = '/data03/fiechter/WC15N_1988-2010/'

his_file = history_base + 'Run_1988/' + 'wc15n_avg_0001.nc'

dset = netCDF4.Dataset(his_file, 'r')

#test_list = []

#for var in variables_list:

#    test_list.append(dset.variables[var][:])

var = variables_list[10]

#loaded_var = dset.variables['CalC'][:]
#var = dset['CalC']
loaded_var = dset.variables[var][:]
#var = dset[var]

mem1 = get_used_mem()

dset.close


mem2 = get_used_mem()


print('memory used to load {0}: {1:.0f} MB'.format(var,mem1-mem0))
#print('memory used to load {0}: {1:.0f} MB'.format(var,mem2-mem0))


