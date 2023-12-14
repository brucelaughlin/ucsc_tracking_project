# Use the algorithm suggested by Chris, to create a new "psi" grid with
# "correct" mask values, according to our coastline-walking needs

import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt



#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
grid_file_in = 'wc15_grd_no_islands.nc'
mask_file_out = 'mask_psi_bl.p'
#---------------------------------------------------------------------
#---------------------------------------------------------------------





base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_path_in = base_path + grid_directory + grid_file_in

dset = netCDF4.Dataset(grid_path_in, 'r')
rho_mask = np.array(dset['mask_rho'])
dset.close

psi_bl_pre_1 = rho_mask[1:,:] + rho_mask[:-1,:]
psi_bl_pre_2 = psi_bl_pre_1[:,1:] + psi_bl_pre_1[:,:-1]
psi_bl = psi_bl_pre_2 > .5

file = open(mask_file_out,'wb')
pickle.dump(psi_bl,file)
file.close()


